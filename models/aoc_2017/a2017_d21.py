import numpy as np
from typing import Iterator


class ArtBlock:
    def __init__(self, pattern: np.ndarray) -> None:
        self._pattern = pattern

    @property
    def num_cells_on(self) -> int:
        return np.sum(self._pattern)

    @property
    def size(self) -> int:
        return self._pattern.shape[0]

    def subdivide(self, size: int) -> Iterator["ArtBlock"]:
        for i in range(self.size // size):
            for j in range(self.size // size):
                yield ArtBlock(
                    self._pattern[i * size : (i + 1) * size, j * size : (j + 1) * size]
                )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ArtBlock):
            return NotImplemented
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        candidates = set()
        pattern = self._pattern
        for _ in range(4):
            candidates.add(hash(pattern.tostring()))
            candidates.add(hash(np.fliplr(pattern).tostring()))
            pattern = np.rot90(pattern)
        return min(candidates)


class FractalArt:
    def __init__(
        self, initial_pattern: ArtBlock, rules: dict[ArtBlock, ArtBlock]
    ) -> None:
        self._initial_pattern = initial_pattern
        self._rules = rules

    def num_cells_on_after_iterations(self, num_iterations: int) -> int:
        pattern = self._initial_pattern
        for _ in range(num_iterations):
            size = 2 if pattern.size % 2 == 0 else 3
            num_blocks_per_row = pattern.size // size
            new_pattern_size = num_blocks_per_row * (size + 1)
            new_pattern = np.zeros((new_pattern_size, new_pattern_size), dtype=int)
            for i, block in enumerate(pattern.subdivide(size)):
                new_pattern[
                    (i // num_blocks_per_row)
                    * (size + 1) : (i // num_blocks_per_row + 1)
                    * (size + 1),
                    (i % num_blocks_per_row)
                    * (size + 1) : (i % num_blocks_per_row + 1)
                    * (size + 1),
                ] = self._rules[block]._pattern
            pattern = ArtBlock(new_pattern)
        return pattern.num_cells_on
