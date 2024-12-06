import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import PatrolArea, PatrolGuard

_AREA = PatrolArea(
    width=10,
    height=10,
    obstacles={
        Vector2D(x=0, y=8),
        Vector2D(x=1, y=6),
        Vector2D(x=2, y=3),
        Vector2D(x=4, y=0),
        Vector2D(x=6, y=9),
        Vector2D(x=7, y=4),
        Vector2D(x=8, y=7),
        Vector2D(x=9, y=1),
    },
)


@pytest.mark.parametrize(
    "guard_pos, guard_dir, expected_distance",
    [
        (Vector2D(0, 0), CardinalDirection.EAST, 4),
        (Vector2D(4, 6), CardinalDirection.NORTH, 6),
    ],
)
def test_patrol_area_keeps_track_of_distance_to_next_obstacle(
    guard_pos, guard_dir, expected_distance
):
    guard = PatrolGuard(guard_pos, guard_dir)
    assert expected_distance == _AREA.distance_to_next_obstacle(guard)


@pytest.mark.parametrize(
    "guard_pos, guard_dir, expected_distance",
    [
        (Vector2D(0, 0), CardinalDirection.WEST, -1),
        (Vector2D(4, 6), CardinalDirection.SOUTH, -4),
    ],
)
def test_patrol_area_keeps_returns_negative_distance_from_guard_to_edge(
    guard_pos, guard_dir, expected_distance
):
    guard = PatrolGuard(guard_pos, guard_dir)
    assert expected_distance == _AREA.distance_to_next_obstacle(guard)
