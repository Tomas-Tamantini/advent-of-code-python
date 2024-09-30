from dataclasses import dataclass
from typing import Iterator, Optional
from models.common.io import CharacterGrid
from models.common.vectors import Vector2D, CardinalDirection


class PipeSegment:
    def __init__(self, direction_a: CardinalDirection, direction_b: CardinalDirection):
        self._directions = {direction_a, direction_b}

    def can_enter_from(self, direction: CardinalDirection) -> bool:
        return direction in self._directions

    def exit_direction(self, enter_direction: CardinalDirection) -> CardinalDirection:
        return next(iter(self._directions - {enter_direction.reverse()}))


_STARTING_TILE = "S"
_SEGMENTS = {
    "|": PipeSegment(CardinalDirection.NORTH, CardinalDirection.SOUTH),
    "-": PipeSegment(CardinalDirection.WEST, CardinalDirection.EAST),
    "L": PipeSegment(CardinalDirection.NORTH, CardinalDirection.EAST),
    "J": PipeSegment(CardinalDirection.NORTH, CardinalDirection.WEST),
    "7": PipeSegment(CardinalDirection.SOUTH, CardinalDirection.WEST),
    "F": PipeSegment(CardinalDirection.SOUTH, CardinalDirection.EAST),
}


@dataclass
class _AnimalState:
    position: Vector2D
    direction: CardinalDirection
    segment: PipeSegment

    def next_direction(self) -> CardinalDirection:
        return self.segment.exit_direction(enter_direction=self.direction)


class PipeMaze:
    def __init__(self, grid: CharacterGrid):
        self._grid = grid

    def _starting_position(self) -> Vector2D:
        return next(self._grid.positions_with_value(_STARTING_TILE))

    def _segment_at(self, position: Vector2D) -> Optional[PipeSegment]:
        char_at_position = self._grid.tiles.get(position, ".")
        return _SEGMENTS.get(char_at_position)

    def _second_animal_state(self) -> _AnimalState:
        position = self._starting_position()
        for direction in CardinalDirection:
            next_position = position.move(direction, y_grows_down=True)
            next_segment = self._segment_at(next_position)
            if next_segment and next_segment.can_enter_from(direction.reverse()):
                return _AnimalState(next_position, direction, next_segment)

    def _next_state(self, current_state: _AnimalState) -> _AnimalState:
        next_direction = current_state.next_direction()
        next_position = current_state.position.move(next_direction, y_grows_down=True)
        next_segment = self._segment_at(next_position)
        return _AnimalState(next_position, next_direction, next_segment)

    def loop_positions(self) -> Iterator[Vector2D]:
        starting_position = self._starting_position()
        yield starting_position
        state = self._second_animal_state()
        while state.position != starting_position:
            yield state.position
            state = self._next_state(state)
