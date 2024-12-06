from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class JigsawPieceOrientation:
    num_quarter_turns: int
    is_flipped: bool

    @staticmethod
    def all_possible_orientations():
        for num_quarter_turns in range(4):
            for is_flipped in (False, True):
                yield JigsawPieceOrientation(num_quarter_turns, is_flipped)

    def transform(self, matrix: np.array) -> np.array:
        new_matrix = matrix.copy()
        if self.is_flipped:
            new_matrix = np.fliplr(new_matrix)
        return np.rot90(new_matrix, k=self.num_quarter_turns, axes=(1, 0))
