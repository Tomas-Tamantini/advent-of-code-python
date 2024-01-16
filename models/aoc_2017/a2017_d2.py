import numpy as np


class Spreadsheet:
    def __init__(self, numbers: np.ndarray):
        self.numbers = numbers

    @staticmethod
    def _difference_between_max_and_min_in_row(row: np.ndarray) -> int:
        return row.max() - row.min()

    def checksum_min_max(self) -> int:
        return sum(
            self._difference_between_max_and_min_in_row(row) for row in self.numbers
        )

    @staticmethod
    def _division_result_in_row(row: np.ndarray) -> int:
        for i, n in enumerate(row):
            for m in row[i + 1 :]:
                if n % m == 0:
                    return n // m
                elif m % n == 0:
                    return m // n
        return 0

    def checksum_divisibility(self) -> int:
        return sum(self._division_result_in_row(row) for row in self.numbers)
