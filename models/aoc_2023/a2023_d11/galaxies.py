from typing import Iterator
from bisect import bisect_left
from itertools import combinations
from models.common.vectors import Vector2D


class Galaxies:
    def __init__(self, galaxy_positions: set[Vector2D]) -> None:
        self._positions = galaxy_positions
        self._non_empty_rows = sorted({position.y for position in galaxy_positions})
        self._non_empty_columns = sorted({position.x for position in galaxy_positions})

    def pairwise_galaxies(self) -> Iterator[tuple[Vector2D, Vector2D]]:
        for pair in combinations(self._positions, 2):
            yield pair

    @staticmethod
    def _amount_in_between(
        sorted_list: list[int], number_start: int, number_end: int
    ) -> int:
        start_index = bisect_left(sorted_list, number_start)
        end_index = bisect_left(sorted_list, number_end)
        return end_index - start_index - 1

    def num_empty_rows_between(self, row_a: int, row_b: int) -> int:
        num_rows = abs(row_a - row_b) - 1
        num_non_empty = self._amount_in_between(
            sorted_list=self._non_empty_rows,
            number_start=min(row_a, row_b),
            number_end=max(row_a, row_b),
        )
        return num_rows - num_non_empty

    def num_empty_columns_between(self, column_a: int, column_b: int) -> int:
        num_columns = abs(column_a - column_b) - 1
        num_non_empty = self._amount_in_between(
            sorted_list=self._non_empty_columns,
            number_start=min(column_a, column_b),
            number_end=max(column_a, column_b),
        )
        return num_columns - num_non_empty

    def distance_between(
        self, position_a: Vector2D, position_b: Vector2D, expansion_rate: int
    ) -> int:
        num_empty_cols = self.num_empty_columns_between(position_a.x, position_b.x)
        num_empty_rows = self.num_empty_rows_between(position_a.y, position_b.y)
        return position_a.manhattan_distance(position_b) + (expansion_rate - 1) * (
            num_empty_cols + num_empty_rows
        )
