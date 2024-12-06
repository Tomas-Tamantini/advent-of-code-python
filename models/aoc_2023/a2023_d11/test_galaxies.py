import pytest

from models.common.vectors import Vector2D

from .galaxies import Galaxies


def test_galaxies_loop_through_every_pair_of_galaxies():
    positions = {Vector2D(0, 0), Vector2D(1, 1), Vector2D(2, 2), Vector2D(3, 3)}
    galaxies = Galaxies(positions)
    pairs = list(galaxies.pairwise_galaxies())
    assert len(pairs) == 6


def test_galaxies_keep_track_of_empty_rows():
    positions = {Vector2D(10, 20), Vector2D(100, 13), Vector2D(1000, 22)}
    galaxies = Galaxies(positions)
    assert galaxies.num_empty_rows_between(row_a=13, row_b=20) == 6
    assert galaxies.num_empty_rows_between(row_a=22, row_b=13) == 7
    assert galaxies.num_empty_rows_between(row_a=20, row_b=22) == 1


def test_galaxies_keep_track_of_empty_columns():
    positions = {Vector2D(10, 20), Vector2D(100, 13), Vector2D(1000, 22)}
    galaxies = Galaxies(positions)
    assert galaxies.num_empty_columns_between(column_a=100, column_b=10) == 89
    assert galaxies.num_empty_columns_between(column_a=100, column_b=1000) == 899
    assert galaxies.num_empty_columns_between(column_a=1000, column_b=10) == 988


@pytest.mark.parametrize(
    "expansion_rate, distance", [(1, 7), (2, 9), (1000000, 2000005)]
)
def test_distance_between_galaxies_takes_expansion_rate_into_consideration(
    expansion_rate, distance
):
    positions = {
        Vector2D(x=7, y=1),
        Vector2D(x=1, y=5),
        Vector2D(x=4, y=9),
        Vector2D(x=9, y=6),
        Vector2D(x=0, y=9),
        Vector2D(x=6, y=4),
        Vector2D(x=3, y=0),
        Vector2D(x=0, y=2),
        Vector2D(x=7, y=8),
    }
    galaxies = Galaxies(positions)

    assert distance == galaxies.distance_between(
        Vector2D(x=4, y=9), Vector2D(1, 5), expansion_rate
    )
