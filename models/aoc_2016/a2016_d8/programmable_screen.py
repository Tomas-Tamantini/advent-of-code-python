import numpy as np


class ProgrammableScreen:
    def __init__(self, width: int, height: int) -> None:
        self.screen = np.zeros((height, width), dtype=int)

    def rect(self, width: int, height: int) -> None:
        self.screen[:height, :width] = 1

    def number_of_lit_pixels(self) -> int:
        return np.sum(self.screen)

    def rotate_row(self, row: int, offset: int) -> None:
        self.screen[row] = np.roll(self.screen[row], offset)

    def rotate_column(self, column: int, offset: int) -> None:
        self.screen[:, column] = np.roll(self.screen[:, column], offset)

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self.screen)
