from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class ReindeerRacer:
    position: Vector2D
    direction: CardinalDirection

    def turn_left(self) -> "ReindeerRacer":
        return ReindeerRacer(self.position, self.direction.turn_left())

    def turn_right(self) -> "ReindeerRacer":
        return ReindeerRacer(self.position, self.direction.turn_right())
