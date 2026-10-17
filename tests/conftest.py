import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import db
import dice


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    db.Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    engine.dispose()


@pytest.fixture(autouse=True)
def isolated_files(tmp_path, monkeypatch):
    db_path = (tmp_path / "stats.db").as_posix()
    monkeypatch.setattr(db, "DB_URL", f"sqlite:///{db_path}")
    monkeypatch.setattr(dice, "LOG_FILE", str(tmp_path / "app.log"))

    yield

    for handler in dice.logger.handlers[:]:
        dice.logger.removeHandler(handler)
        handler.close()
