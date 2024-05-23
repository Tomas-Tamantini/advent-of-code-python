from typing import Iterator
from models.common.vectors import Vector2D, CardinalDirection


class TreeHeightMap:
    def __init__(self, tree_heights: list[list[int]]) -> None:
        self._heights = tree_heights
        self._width = len(tree_heights[0])
        self._height = len(tree_heights)

    def _column_range(self, looking_direction: CardinalDirection) -> range:
        if looking_direction == CardinalDirection.EAST:
            return range(self._width)
        else:
            return range(self._width - 1, -1, -1)

    def _row_range(self, looking_direction: CardinalDirection) -> range:
        if looking_direction == CardinalDirection.SOUTH:
            return range(self._height)
        else:
            return range(self._height - 1, -1, -1)

    def visible_trees(self, looking_direction: CardinalDirection) -> Iterator[Vector2D]:
        if looking_direction.is_horizontal:
            for row in range(self._height):
                tallest_so_far = -1
                for column in self._column_range(looking_direction):
                    if self._heights[row][column] > tallest_so_far:
                        tallest_so_far = self._heights[row][column]
                        yield Vector2D(column, row)
        else:
            for column in range(self._width):
                tallest_so_far = -1
                for row in self._row_range(looking_direction):
                    if self._heights[row][column] > tallest_so_far:
                        tallest_so_far = self._heights[row][column]
                        yield Vector2D(column, row)
