from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class PatrolGuard:
    position: Vector2D
    direction: CardinalDirection

    def move_and_turn_right(self, num_steps: int) -> "PatrolGuard":
        return PatrolGuard(
            position=self.position.move(self.direction, num_steps, y_grows_down=True),
            direction=self.direction.turn_right(),
        )
