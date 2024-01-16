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
