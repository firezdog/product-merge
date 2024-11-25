from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator


ENGINE: Engine = None


def get_engine(db_path: str = "sqlite:////home/app/example.db") -> Generator[Session, None, None]:
    global ENGINE
    if not ENGINE:
        ENGINE = create_engine(db_path, echo=True)

    SQLModel.metadata.create_all(ENGINE)
    return ENGINE
