from dataclasses import dataclass
from typing import Protocol
from models.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class Submarine:
    position: Vector2D = Vector2D(0, 0)
    aim: int = 0


class SubmarineNavigationInstruction(Protocol):
    def execute(self, submarine: Submarine) -> Submarine: ...


@dataclass(frozen=True)
class MoveSubmarineInstruction:
    direction: CardinalDirection
    distance: int

    def execute(self, submarine: Submarine) -> Submarine:
        new_pos = submarine.position.move(
            self.direction, self.distance, y_grows_down=True
        )
        return Submarine(position=new_pos, aim=submarine.aim)


@dataclass(frozen=True)
class IncrementAimInstruction:
    increment: int

    def execute(self, submarine: Submarine) -> Submarine:
        return Submarine(
            position=submarine.position, aim=submarine.aim + self.increment
        )


@dataclass(frozen=True)
class MoveSubmarineWithAimInstruction:
    distance: int

    def execute(self, submarine: Submarine) -> Submarine:
        new_pos = Vector2D(
            submarine.position.x + self.distance,
            submarine.position.y + self.distance * submarine.aim,
        )
        return Submarine(position=new_pos, aim=submarine.aim)
