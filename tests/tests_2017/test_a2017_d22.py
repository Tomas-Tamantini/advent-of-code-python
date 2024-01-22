import pytest
from models.aoc_2017 import GridCluster
from models.vectors import Vector2D, CardinalDirection


@pytest.mark.parametrize(
    "num_steps, num_infections",
    [(0, 0), (1, 1), (2, 1), (7, 5), (70, 41), (10000, 5587)],
)
def test_grid_keeps_track_of_how_many_infections_were_caused(num_steps, num_infections):
    cluster = GridCluster(
        currently_infected={Vector2D(2, 0), Vector2D(0, 1)},
        carrier_position=Vector2D(1, 1),
        carrier_direction=CardinalDirection.SOUTH,
    )
    assert cluster.total_number_of_infections_caused(num_steps) == num_infections
