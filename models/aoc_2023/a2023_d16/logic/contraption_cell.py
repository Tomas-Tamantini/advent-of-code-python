from typing import Protocol, Iterator
from models.common.vectors import CardinalDirection


class ContraptionCell(Protocol):
    def next_directions(
        self, beam_direction: CardinalDirection
    ) -> Iterator[CardinalDirection]: ...


class EmptyCell:
    def next_directions(
        self, beam_direction: CardinalDirection
    ) -> Iterator[CardinalDirection]:
        yield beam_direction


class Mirror:
    def __init__(self, is_upward_diagonal: bool) -> None:
        self._is_upward_diagonal = is_upward_diagonal

    def next_directions(
        self, beam_direction: CardinalDirection
    ) -> Iterator[CardinalDirection]:
        if beam_direction.is_horizontal == self._is_upward_diagonal:
            yield beam_direction.turn_left()
        else:
            yield beam_direction.turn_right()


class Splitter:
    def __init__(self, is_horizontal: bool) -> None:
        self._is_horizontal = is_horizontal

    def next_directions(
        self, beam_direction: CardinalDirection
    ) -> Iterator[CardinalDirection]:
        if beam_direction.is_horizontal == self._is_horizontal:
            yield beam_direction
        else:
            yield beam_direction.turn_left()
            yield beam_direction.turn_right()
