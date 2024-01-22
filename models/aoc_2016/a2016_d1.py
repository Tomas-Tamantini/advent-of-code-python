from dataclasses import dataclass
from models.vectors import CardinalDirection, Vector2D, TurnDirection
from typing import Iterator


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
        self._direction = self._direction.turn(instruction.turn)
        for _ in range(instruction.steps):
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
