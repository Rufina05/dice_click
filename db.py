from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_URL = "sqlite:///stats.db"
MIN_SIDES = 2


class Base(DeclarativeBase):
    pass


class Throw(Base):
    __tablename__ = "throws"

    id: Mapped[int] = mapped_column(primary_key=True)
    sides: Mapped[int]
    value: Mapped[int]


@contextmanager
def get_session() -> Iterator[Session]:
    engine = create_engine(DB_URL)
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose() 
