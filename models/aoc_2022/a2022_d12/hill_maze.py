from math import inf
from typing import Iterator
from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from models.common.graphs import explore_with_bfs


class HillMaze:
    def __init__(self, grid: CharacterGrid) -> None:
        self._grid = grid

    def _char_height(self, position: Vector2D) -> int:
        char = self._grid.tiles[position]
        if char == "S":
            char = "a"
        elif char == "E":
            char = "z"
        return ord(char)

    def _height_difference(self, origin: Vector2D, destination: Vector2D) -> int:
        return self._char_height(destination) - self._char_height(origin)

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions(include_diagonals=False):
            if (
                self._grid.contains(neighbor)
                and self._height_difference(node, neighbor) >= -1
            ):
                yield neighbor

    def min_num_steps_to_destination(
        self, inital_height: chr, finish_height: chr
    ) -> int:
        min_steps = inf
        for end in self._grid.positions_with_value(finish_height):
            for node, distance in explore_with_bfs(self, initial_node=end):
                if self._grid.tiles[node] == inital_height:
                    min_steps = min(min_steps, distance)
        return min_steps
