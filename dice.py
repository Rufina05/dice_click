import logging
import random

import click
from sqlalchemy.exc import SQLAlchemyError

from dal import count_throws, save_throws
from db import MIN_SIDES, get_session

LOG_FILE = "app.log"
MIN_COUNT = 1

logger = logging.getLogger("dice")


def setup_logging() -> None:
    for old_handler in logger.handlers[:]:
        logger.removeHandler(old_handler)
        old_handler.close()

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def roll_dice(count: int, sides: int) -> list[int]:
    if count < MIN_COUNT:
        raise ValueError(f"--count must be >= {MIN_COUNT}")
    if sides < MIN_SIDES:
        raise ValueError(f"--sides must be >= {MIN_SIDES}")
    return [random.randint(1, sides) for _ in range(count)]


def format_stat(count: int, total: int, view: str | None) -> str:
    percent = count / total * 100 if total else 0
    if view == "abs":
        return f"{count}"
    if view == "rel":
        return f"{percent:.1f}%"
    return f"{count} ({percent:.1f}%)" 


def format_stats(counts: dict[int, dict[int, int]], view: str | None) -> list[str]:
    lines = []
    for sides in sorted(counts):
        total = sum(counts[sides].values())
        parts = [
            f"{value} — {format_stat(counts[sides].get(value, 0), total, view)}"
            for value in range(1, sides + 1)
        ]
        lines.append(f"d{sides}: " + ", ".join(parts))
    return lines


@click.group()
def cli() -> None:
    setup_logging()


@cli.command()
@click.option("--count", "-c", type=int, default=1, help="How many dice to roll")
@click.option("--sides", "-s", type=int, default=6, help="How many sides each die has")
def roll(count: int, sides: int) -> None:
    try:
        values = roll_dice(count, sides)
    except ValueError as error:
        logger.warning("roll: invalid arguments, count=%s sides=%s", count, sides)
        raise click.BadParameter(str(error)) from error

    logger.info("roll: count=%d sides=%d values=%s", count, sides, values)
    click.echo(f"🎲 {values}")
    click.echo(f"Sum: {sum(values)}")

    try:
        with get_session() as session:
            save_throws(session, sides, values)
    except SQLAlchemyError as error:
        logger.exception("roll: database error")
        raise click.ClickException("failed to save throw to database") from error


@cli.command()
@click.option("--view", type=click.Choice(["abs", "rel"]), default=None)
def stats(view: str | None) -> None:
    try:
        with get_session() as session:
            counts = count_throws(session)
    except SQLAlchemyError as error:
        logger.exception("stats: database error")
        raise click.ClickException("failed to read statistics") from error

    logger.info("stats: view=%s, dice kinds=%d", view, len(counts))
    if not counts:
        click.echo("No throws yet")
        return

    for line in format_stats(counts, view):
        click.echo(line)
