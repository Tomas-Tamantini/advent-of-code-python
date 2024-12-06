from typing import Iterator
from models.common.vectors import Vector2D
from .patrol_area import PatrolArea
from .patrol_guard import PatrolGuard


def _guard_states(area: PatrolArea, guard: PatrolGuard) -> Iterator[PatrolGuard]:
    while not area.is_out_of_bounds(guard.position):
        yield guard
        position_in_front = guard.position_in_front()
        if area.is_obstacle(position_in_front):
            guard = guard.turn_right()
        else:
            guard = guard.move_forward()


def patrol_route(area: PatrolArea, guard: PatrolGuard) -> Iterator[Vector2D]:
    for guard in _guard_states(area, guard):
        yield guard.position


def guard_goes_into_loop(area: PatrolArea, guard: PatrolGuard) -> bool:
    visited_states = set()
    for guard in _guard_states(area, guard):
        if guard in visited_states:
            return True
        visited_states.add(guard)
    return False
