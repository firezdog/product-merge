import json
from datetime import datetime, timezone

from sqlalchemy import Table, exists, func, update, select, insert, delete
from sqlmodel import Session

from connection import get_engine
from model import Product


def create_sample_products(session: Session):
    session.exec(delete(Product.__table__))

    with open('sample_products.jsonlines', 'r') as fp:
        for line in fp.readlines():
            product = json.loads(line)
            session.add(Product(**product))

    session.commit()


def update_sample_products(session: Session):
    vendor_updates = Product.create_temp_table(engine=session.get_bind(), temp_name='temp_vendor')
    supplier_updates = Product.create_temp_table(engine=session.get_bind(), temp_name='temp_supplier')
    with open('sample_product_updates.jsonlines', 'r') as fp:
        for line in fp.readlines():
            product = json.loads(line)
            if not product.get('id'):
                session.exec(insert(vendor_updates).values(**product))
            else:
                session.exec(insert(supplier_updates).values(**product))
    session.commit()

    main_table: Table = Product.__table__
    update_values = {
        col.name: vendor_updates.c[col.name]
        for col in main_table.columns
        if col.name not in {"id", "created_at"}  # Exclude `id` and `created_at` from updates
    }
    update_values["updated_at"] = datetime.now(tz=timezone.utc)

    update_stmt = (
        update(main_table)
        .where(main_table.c.supplier_id == vendor_updates.c.supplier_id)
        .values(**update_values)
    )
    session.exec(update_stmt)

    insert_stmt = insert(main_table).from_select(
        [col.name for col in main_table.columns],  # Insert all columns dynamically
        select(vendor_updates).where(
            ~exists().where(main_table.c.supplier_id == vendor_updates.c.supplier_id),
        ),
    )
    session.exec(insert_stmt)
    session.commit()

    update_values = {
        col.name: func.coalesce(supplier_updates.c[col.name], main_table.c[col.name])
        for col in main_table.columns
        if col.name not in {"id", "created_at"}
    }
    update_values["updated_at"] = datetime.now(tz=timezone.utc)
    update_stmt = (
        update(main_table)
        .where(main_table.c.id == supplier_updates.c.id)  # Match on internal `id`
        .values(**update_values)
    )
    session.exec(update_stmt)
    session.commit()

    vendor_updates.drop(bind=session.get_bind())
    supplier_updates.drop(bind=session.get_bind())


if __name__ == '__main__':
    engine = get_engine()
    with Session(engine) as session:
        # uncomment to populate db
        create_sample_products(session=session)
        update_sample_products(session=session)
