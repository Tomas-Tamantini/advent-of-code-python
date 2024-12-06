from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D

from .patrol_area import PatrolArea
from .patrol_guard import PatrolGuard


@dataclass(frozen=True)
class _PatrolSegment:
    start_position: Vector2D
    direction: CardinalDirection
    length: int

    def positions(self) -> Iterator[Vector2D]:
        position = self.start_position
        for _ in range(self.length):
            yield position
            position = position.move(self.direction, y_grows_down=True)


def _patrol_segments(area: PatrolArea, guard: PatrolGuard) -> Iterator[_PatrolSegment]:
    current_guard = guard
    while True:
        distance_to_next_obstacle = area.distance_to_next_obstacle(current_guard)
        if distance_to_next_obstacle < 0:
            yield _PatrolSegment(
                start_position=current_guard.position,
                direction=current_guard.direction,
                length=-distance_to_next_obstacle,
            )
            break
        else:
            yield _PatrolSegment(
                start_position=current_guard.position,
                direction=current_guard.direction,
                length=distance_to_next_obstacle,
            )
            current_guard = current_guard.move_and_turn_right(
                distance_to_next_obstacle - 1
            )


def patrol_route(area: PatrolArea, guard: PatrolGuard) -> Iterator[Vector2D]:
    for segment in _patrol_segments(area, guard):
        yield from segment.positions()


def guard_goes_into_loop(area: PatrolArea, guard: PatrolGuard) -> bool:
    visited_states = set()
    for segment in _patrol_segments(area, guard):
        if segment in visited_states:
            return True
        visited_states.add(segment)
    return False
