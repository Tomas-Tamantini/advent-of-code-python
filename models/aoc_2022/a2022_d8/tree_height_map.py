from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


class TreeHeightMap:
    def __init__(self, tree_heights: list[list[int]]) -> None:
        self._heights = tree_heights
        self._width = len(tree_heights[0])
        self._height = len(tree_heights)

    def all_positions(self) -> Iterator[Vector2D]:
        for row in range(self._height):
            for column in range(self._width):
                yield Vector2D(column, row)

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

    def _is_out_of_bounds(self, position: Vector2D) -> bool:
        return not (0 <= position.x < self._width and 0 <= position.y < self._height)

    def visible_trees_from_position(
        self, position: Vector2D, looking_direction: CardinalDirection
    ) -> Iterator[Vector2D]:
        my_height = self._heights[position.y][position.x]
        current_position = position
        while True:
            current_position = current_position.move(
                looking_direction, y_grows_down=True
            )
            if self._is_out_of_bounds(current_position):
                break
            yield current_position
            new_height = self._heights[current_position.y][current_position.x]
            if new_height >= my_height:
                break
