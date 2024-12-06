import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import PatrolArea, PatrolGuard, patrol_route, guard_goes_into_loop

_OBSTACLES = {
    Vector2D(x=0, y=8),
    Vector2D(x=1, y=6),
    Vector2D(x=2, y=3),
    Vector2D(x=4, y=0),
    Vector2D(x=6, y=9),
    Vector2D(x=7, y=4),
    Vector2D(x=8, y=7),
    Vector2D(x=9, y=1),
}

_GUARD = PatrolGuard(position=Vector2D(x=4, y=6), direction=CardinalDirection.NORTH)


def test_patrol_route_returns_every_position_of_guard():
    area = PatrolArea(width=10, height=10, obstacles=_OBSTACLES)
    positions = set(patrol_route(area, _GUARD))
    assert len(positions) == 41


def test_patrol_guard_does_not_go_into_loop_if_they_leave_area():
    area = PatrolArea(width=10, height=10, obstacles=_OBSTACLES)
    assert not guard_goes_into_loop(area, _GUARD)


@pytest.mark.parametrize(
    "extra_obstacle",
    [
        Vector2D(x=3, y=6),
        Vector2D(x=6, y=7),
        Vector2D(x=3, y=8),
    ],
)
def test_patrol_guard_goes_into_loop_if_stuck_inside_area(extra_obstacle):
    area = PatrolArea(width=10, height=10, obstacles=_OBSTACLES | {extra_obstacle})
    assert guard_goes_into_loop(area, _GUARD)
