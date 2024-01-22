from models.vectors import Vector2D, CardinalDirection


class LangtonsAnt:
    def __init__(
        self,
        ant_position: Vector2D,
        ant_direction: CardinalDirection,
        initial_on_squares: set[Vector2D],
    ) -> None:
        self._ant_position = ant_position
        self._ant_direction = ant_direction
        self._on_squares = initial_on_squares

    @property
    def position(self) -> Vector2D:
        return self._ant_position

    @property
    def direction(self) -> CardinalDirection:
        return self._ant_direction

    @property
    def on_squares(self) -> set[Vector2D]:
        return self._on_squares

    def walk(self) -> None:
        if self._ant_position in self._on_squares:
            self._ant_direction = self._ant_direction.turn_left()
        else:
            self._ant_direction = self._ant_direction.turn_right()
        self._on_squares ^= {self._ant_position}
        self._ant_position = self._ant_position.move(self._ant_direction)
