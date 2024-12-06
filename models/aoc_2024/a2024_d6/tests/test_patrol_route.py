from models.common.vectors import Vector2D, CardinalDirection
from ..logic import PatrolArea, PatrolGuard, patrol_route


def test_patrol_route_returns_every_position_of_guard():
    guard = PatrolGuard(position=Vector2D(x=4, y=6), direction=CardinalDirection.NORTH)
    area = PatrolArea(
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
    positions = set(patrol_route(area, guard))
    assert len(positions) == 41
