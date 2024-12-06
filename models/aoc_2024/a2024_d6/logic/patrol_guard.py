from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class PatrolGuard:
    position: Vector2D
    direction: CardinalDirection

    def position_in_front(self) -> Vector2D:
        return self.position.move(self.direction, y_grows_down=True)

    def move_forward(self) -> "PatrolGuard":
        return PatrolGuard(position=self.position_in_front(), direction=self.direction)

    def turn_right(self) -> "PatrolGuard":
        return PatrolGuard(
            position=self.position, direction=self.direction.turn_right()
        )
