from typing import Iterator
from models.common.vectors import Vector2D
from .patrol_area import PatrolArea
from .patrol_guard import PatrolGuard


def patrol_route(area: PatrolArea, guard: PatrolGuard) -> Iterator[Vector2D]:
    while not area.is_out_of_bounds(guard.position):
        yield guard.position
        position_in_front = guard.position_in_front()
        if area.is_obstacle(position_in_front):
            guard = guard.turn_right()
        else:
            guard = guard.move_forward()
