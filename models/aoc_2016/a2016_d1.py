from dataclasses import dataclass
from models.vectors import CardinalDirection, Vector2D
from enum import Enum
from typing import Iterator


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


class Turtle:
    def __init__(self, initial_direction: CardinalDirection) -> None:
        self._direction = initial_direction
        self._path_history = [Vector2D(0, 0)]

    @property
    def position(self) -> Vector2D:
        return self._path_history[-1]

    @property
    def direction(self) -> CardinalDirection:
        return self._direction

    def move(self, instruction: TurtleInstruction) -> None:
        self._direction = instruction.turn.transform_direction(self._direction)
        for step in range(instruction.steps):
            self._path_history.append(self.position.move(self._direction))

    @property
    def path_history(self) -> list[Vector2D]:
        return self._path_history

    def path_self_intersections(self) -> Iterator[Vector2D]:
        points_visited = set()
        for point in self._path_history:
            if point in points_visited:
                yield point
            points_visited.add(point)
