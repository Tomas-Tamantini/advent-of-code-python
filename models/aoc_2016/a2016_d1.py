from dataclasses import dataclass
from models.vectors import CardinalDirection, Vector2D
from enum import Enum


class TurnDirection(Enum):
    LEFT = "L"
    RIGHT = "R"

    def transform_direction(self, direction: CardinalDirection) -> CardinalDirection:
        if self == TurnDirection.LEFT:
            return direction.turn_left()
        else:
            return direction.turn_right()


@dataclass(frozen=True)
class TurtleInstruction:
    turn: TurnDirection
    steps: int


def turtle_destination(
    instructions: list[TurtleInstruction],
    initial_direction: CardinalDirection = CardinalDirection.NORTH,
) -> Vector2D:
    position = Vector2D(0, 0)
    direction = initial_direction
    for instruction in instructions:
        direction = instruction.turn.transform_direction(direction)
        position = position.move(direction, instruction.steps)
    return position
