from typing import Iterator
from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from models.common.graphs import min_path_length_with_bfs


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
                and self._height_difference(node, neighbor) <= 1
            ):
                yield neighbor

    def min_num_steps_to_destination(self) -> int:
        initial_node = next(self._grid.positions_with_value("S"))
        final_node = next(self._grid.positions_with_value("E"))
        return min_path_length_with_bfs(
            self,
            initial_node,
            is_final_state=lambda node: node == final_node,
        )
