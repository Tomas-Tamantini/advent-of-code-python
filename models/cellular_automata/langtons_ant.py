from dataclasses import dataclass
from models.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class AntState:
    position: Vector2D
    direction: CardinalDirection


class LangtonsAnt:
    def __init__(
        self,
        ant_state: AntState,
        initial_on_squares: set[Vector2D],
    ) -> None:
        self._ant_state = ant_state
        self._on_squares = initial_on_squares

    @property
    def position(self) -> Vector2D:
        return self._ant_state.position

    @property
    def direction(self) -> CardinalDirection:
        return self._ant_state.direction

    @property
    def on_squares(self) -> set[Vector2D]:
        return self._on_squares

    def walk(self) -> None:
        if self._ant_state.position in self._on_squares:
            new_direction = self._ant_state.direction.turn_left()
        else:
            new_direction = self._ant_state.direction.turn_right()
        self._on_squares ^= {self._ant_state.position}
        new_position = self._ant_state.position.move(new_direction)
        self._ant_state = AntState(new_position, new_direction)
