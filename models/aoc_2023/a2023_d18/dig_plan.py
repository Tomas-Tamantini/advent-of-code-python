from dataclasses import dataclass
from typing import Iterable, Iterator

from models.common.vectors import CardinalDirection, Polygon, Vector2D


@dataclass(frozen=True)
class DiggerInstruction:
    direction: CardinalDirection
    num_steps: int

    def move(self, digger_position: Vector2D) -> Vector2D:
        return digger_position.move(self.direction, self.num_steps)


class DigPlan:
    def __init__(self, instructions: Iterable[DiggerInstruction]) -> None:
        self._instructions = instructions

    def _dig_vertices(self) -> Iterator[Vector2D]:
        digger_position = Vector2D(0, 0)
        yield digger_position
        for instruction in self._instructions:
            digger_position = instruction.move(digger_position)
            yield digger_position

    def dig_area(self) -> int:
        polygon = Polygon(list(self._dig_vertices()))
        return polygon.num_grid_points_on_perimeter() + polygon.num_grid_points_inside()
