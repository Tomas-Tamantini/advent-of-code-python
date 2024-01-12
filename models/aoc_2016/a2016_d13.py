from dataclasses import dataclass
from models.vectors import Vector2D, CardinalDirection
from models.graphs import min_path_length_with_bfs
from typing import Callable, ClassVar


def is_wall(position: Vector2D, polynomial_offset: int) -> bool:
    x, y = position.x, position.y
    polynomial = x * x + 3 * x + 2 * x * y + y + y * y + polynomial_offset
    return bin(polynomial).count("1") % 2 == 1


@dataclass(frozen=True)
class MazeCubicle:
    is_wall: ClassVar[Callable[[Vector2D], bool]]
    destination: ClassVar[Vector2D]
    position: Vector2D

    def neighboring_valid_states(self):
        for direction in CardinalDirection:
            new_position = self.position.move(direction)
            if new_position.x < 0 or new_position.y < 0:
                continue
            if MazeCubicle.is_wall(new_position):
                continue
            yield MazeCubicle(position=new_position)

    def is_final_state(self) -> bool:
        return self.position == self.destination

    def length_shortest_path(self) -> int:
        return min_path_length_with_bfs(self)
