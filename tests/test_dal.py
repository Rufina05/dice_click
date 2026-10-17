import pytest
from sqlalchemy import select

from dal import count_throws, save_throws
from db import Throw


def test_save_throws(session):
    saved = save_throws(session, 6, [2, 6, 2])

    rows = session.execute(select(Throw.sides, Throw.value)).all()

    assert saved == 3
    assert sorted(rows) == [(6, 2), (6, 2), (6, 6)]


@pytest.mark.parametrize("values", [[0], [7], [3, 9, 2], [-1]])
def test_save_throws_value_out_of_range(session, values):
    with pytest.raises(ValueError, match="out of range"):
        save_throws(session, 6, values)

    assert session.execute(select(Throw)).all() == []


def test_save_throws_invalid_sides(session):
    with pytest.raises(ValueError, match="sides"):
        save_throws(session, 1, [1])


def test_count_throws_empty_database(session):
    assert count_throws(session) == {}


def test_count_throws_groups_by_sides_and_value(session):
    save_throws(session, 6, [2, 6, 2])
    save_throws(session, 20, [20])

    assert count_throws(session) == {6: {2: 2, 6: 1}, 20: {20: 1}}


def test_count_throws_sums_several_saves(session):
    save_throws(session, 6, [1])
    save_throws(session, 6, [1, 1])

    assert count_throws(session) == {6: {1: 3}}
