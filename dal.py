import logging

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db import MIN_SIDES, Throw

logger = logging.getLogger("dice")


def save_throws(session: Session, sides: int, values: list[int]) -> int:
    if sides < MIN_SIDES:
        raise ValueError(f"sides must be >= {MIN_SIDES}")

    invalid = [value for value in values if not 1 <= value <= sides]
    if invalid:
        logger.warning("save_throws: values out of range, sides=%d", sides)
        raise ValueError(f"values out of range 1..{sides}: {invalid}")

    try:
        session.add_all(Throw(sides=sides, value=value) for value in values)
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise

    logger.info("save_throws: saved %d throws, sides=%d", len(values), sides)
    return len(values)


def count_throws(session: Session) -> dict[int, dict[int, int]]:
    stmt = (
        select(Throw.sides, Throw.value, func.count())
        .group_by(Throw.sides, Throw.value)
        .order_by(Throw.sides, Throw.value)
    )

    counts: dict[int, dict[int, int]] = {}
    for sides, value, count in session.execute(stmt).all():
        counts.setdefault(sides, {})[value] = count
    return counts
