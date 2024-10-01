from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class LightBeam:
    position: Vector2D
    direction: CardinalDirection

    def move_forward(self) -> "LightBeam":
        return LightBeam(
            position=self.position.move(self.direction, y_grows_down=True),
            direction=self.direction,
        )
