from typing import Iterator
import numpy as np
from models.vectors import Vector2D


class BingoBoard:
    def __init__(self, numbers_table: np.ndarray):
        self._numbers_table = numbers_table
        self._marked_positions = set()

    @property
    def num_rows(self) -> int:
        return self._numbers_table.shape[0]

    @property
    def num_columns(self) -> int:
        return self._numbers_table.shape[1]

    def is_winner(self) -> bool:
        for row in range(self.num_rows):
            if all(
                Vector2D(row, column) in self._marked_positions
                for column in range(self.num_columns)
            ):
                return True

        for column in range(self.num_columns):
            if all(
                Vector2D(row, column) in self._marked_positions
                for row in range(self.num_rows)
            ):
                return True

        return False

    def _number_positions(self, number: int) -> Iterator[Vector2D]:
        for position in self._all_positions():
            if self._numbers_table[position.x, position.y] == number:
                yield position

    def mark_number(self, number: int) -> None:
        for position in self._number_positions(number):
            self._marked_positions.add(position)

    def _all_positions(self) -> Iterator[Vector2D]:
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                yield Vector2D(row, column)

    def unmarked_numbers(self) -> Iterator[int]:
        for position in self._all_positions():
            if position not in self._marked_positions:
                yield self._numbers_table[position.x, position.y]


class BingoGame:
    def __init__(self, boards: tuple[BingoBoard]) -> None:
        self._boards = boards

    @property
    def boards(self) -> tuple[BingoBoard]:
        return self._boards

    def winners(self) -> Iterator[BingoBoard]:
        for board in self._boards:
            if board.is_winner():
                yield board

    def is_over(self) -> bool:
        return any(self.winners())

    def draw_number(self, number: int) -> None:
        for board in self._boards:
            board.mark_number(number)
