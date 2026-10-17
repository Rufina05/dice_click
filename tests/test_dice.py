from pathlib import Path
from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

import db
import dice
from dice import cli, format_stat, format_stats, roll_dice


def test_roll_dice_count():
    assert len(roll_dice(5, 6)) == 5


def test_roll_dice_values_in_range():
    values = roll_dice(500, 4)

    assert all(1 <= value <= 4 for value in values)


@pytest.mark.parametrize("count", [0, -1])
def test_roll_dice_invalid_count(count):
    with pytest.raises(ValueError, match="--count"):
        roll_dice(count, 6)


@pytest.mark.parametrize("sides", [1, 0, -5])
def test_roll_dice_invalid_sides(sides):
    with pytest.raises(ValueError, match="--sides"):
        roll_dice(1, sides)


@pytest.mark.parametrize(
    "count, total, view, expected",
    [
        (4, 30, "abs", "4"),
        (4, 30, "rel", "13.3%"),
        (4, 30, None, "4 (13.3%)"),
        (30, 30, "rel", "100.0%"),
        (0, 0, "abs", "0"),
        (0, 0, "rel", "0.0%"),
        (0, 0, None, "0 (0.0%)"),
    ],
)
def test_format_stat(count, total, view, expected):
    assert format_stat(count, total, view) == expected


def test_format_stats_abs_shows_every_face():
    counts = {4: {1: 3, 4: 1}}

    assert format_stats(counts, "abs") == ["d4: 1 — 3, 2 — 0, 3 — 0, 4 — 1"]


def test_format_stats_rel():
    counts = {2: {1: 1, 2: 3}}

    assert format_stats(counts, "rel") == ["d2: 1 — 25.0%, 2 — 75.0%"]


def test_format_stats_both_views():
    counts = {2: {1: 1, 2: 3}}

    assert format_stats(counts, None) == ["d2: 1 — 1 (25.0%), 2 — 3 (75.0%)"]


def test_format_stats_empty():
    assert format_stats({}, None) == []


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_roll(runner, monkeypatch):
    monkeypatch.setattr(dice.random, "randint", MagicMock(side_effect=[2, 6, 2]))

    result = runner.invoke(cli, ["roll", "-c", "3", "-s", "6"])

    assert result.exit_code == 0
    assert "🎲 [2, 6, 2]" in result.output
    assert "Sum: 10" in result.output


def test_cli_roll_defaults(runner):
    result = runner.invoke(cli, ["roll"])

    assert result.exit_code == 0
    assert "Sum:" in result.output


@pytest.mark.parametrize(
    "args, message",
    [
        (["roll", "--count", "0"], "--count must be >= 1"),
        (["roll", "-c", "2", "-s", "1"], "--sides must be >= 2"),
    ],
)
def test_cli_roll_invalid_arguments(runner, args, message):
    result = runner.invoke(cli, args)

    assert result.exit_code != 0
    assert message in result.output


def test_cli_stats_empty_database(runner):
    result = runner.invoke(cli, ["stats"])

    assert result.exit_code == 0
    assert "No throws yet" in result.output


def test_cli_stats_after_roll(runner, monkeypatch):
    monkeypatch.setattr(dice.random, "randint", MagicMock(return_value=3))
    runner.invoke(cli, ["roll", "-c", "2", "-s", "6"])

    result = runner.invoke(cli, ["stats", "--view", "abs"])

    assert result.exit_code == 0
    assert "d6: 1 — 0, 2 — 0, 3 — 2, 4 — 0, 5 — 0, 6 — 0" in result.output


def test_cli_roll_database_error(runner, monkeypatch):
    monkeypatch.setattr(db, "DB_URL", "sqlite:////no_such_dir_xyz/stats.db")

    result = runner.invoke(cli, ["roll"])

    assert result.exit_code == 1
    assert "failed to save throw to database" in result.output


def test_cli_stats_database_error(runner, monkeypatch):
    monkeypatch.setattr(db, "DB_URL", "sqlite:////no_such_dir_xyz/stats.db")

    result = runner.invoke(cli, ["stats"])

    assert result.exit_code == 1
    assert "failed to read statistics" in result.output


def test_cli_writes_log_file(runner):
    runner.invoke(cli, ["roll", "-c", "2"])
    runner.invoke(cli, ["roll", "-c", "0"])

    log_text = Path(dice.LOG_FILE).read_text(encoding="utf-8")

    assert "INFO dice: roll: count=2" in log_text
    assert "INFO dice: save_throws: saved 2 throws" in log_text
    assert "WARNING dice: roll: invalid arguments" in log_text
