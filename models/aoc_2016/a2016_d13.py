from models.common.vectors import Vector2D
from models.common.graphs import min_path_length_with_bfs, explore_with_bfs
from typing import Callable


def is_wall(position: Vector2D, polynomial_offset: int) -> bool:
    x, y = position.x, position.y
    polynomial = x * x + 3 * x + 2 * x * y + y + y * y + polynomial_offset
    return bin(polynomial).count("1") % 2 == 1


class CubicleMaze:
    def __init__(self, is_wall: Callable[[Vector2D], bool], destination: Vector2D):
        self._is_wall = is_wall
        self._destination = destination

    def neighbors(self, position: Vector2D):
        for new_position in position.adjacent_positions():
            if new_position.x < 0 or new_position.y < 0:
                continue
            if self._is_wall(new_position):
                continue
            yield new_position

    def length_shortest_path(self, initial_position: Vector2D) -> int:
        return min_path_length_with_bfs(
            self,
            initial_position,
            is_final_state=lambda p: p == self._destination,
        )

    def number_of_reachable_cubicles(
        self, initial_position: Vector2D, max_steps: int
    ) -> int:
        num_visited = 0
        for _, distance in explore_with_bfs(self, initial_position):
            if distance > max_steps:
                break
            num_visited += 1
        return num_visited
