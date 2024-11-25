from datetime import datetime, timezone
import uuid
from sqlalchemy import Engine, MetaData
from sqlmodel import SQLModel, Field
from typing import Optional


class Product(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    supplier_id: Optional[str] = Field(index=True, nullable=False)
    price: Optional[float]
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), nullable=False)

    @classmethod
    def create_temp_table(cls, engine: Engine, temp_name: str):
        metadata = MetaData()
        temp_table = cls.__table__.tometadata(metadata, name=temp_name)
        metadata.create_all(engine, tables=[temp_table])
        return temp_table
