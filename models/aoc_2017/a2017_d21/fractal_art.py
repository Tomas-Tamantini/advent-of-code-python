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
            candidates.add(hash(pattern.tobytes()))
            candidates.add(hash(np.fliplr(pattern).tobytes()))
            pattern = np.rot90(pattern)
        return min(candidates)


class FractalArt:
    def __init__(
        self, initial_pattern: ArtBlock, rules: dict[ArtBlock, ArtBlock]
    ) -> None:
        self._initial_pattern = initial_pattern
        self._rules = rules

    def _run_iteration(self, pattern: ArtBlock) -> ArtBlock:
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
        return ArtBlock(new_pattern)

    def num_cells_on_after_iterations(self, num_iterations: int) -> int:
        pattern = self._initial_pattern
        while num_iterations > 0 and pattern.size % 2 == 0:
            pattern = self._run_iteration(pattern)
            num_iterations -= 1
        if num_iterations <= 0:
            return pattern.num_cells_on
        else:
            memoized_values: dict[ArtBlock, dict[int, int]] = {}
            return sum(
                self._recursive_num_cells_for_3x3_blocks(
                    sub_block, num_iterations, memoized_values
                )
                for sub_block in pattern.subdivide(3)
            )

    def _recursive_num_cells_for_3x3_blocks(
        self,
        pattern_3x3: ArtBlock,
        num_iterations: int,
        memoized_values: dict[ArtBlock, dict[int, int]],
    ) -> int:
        if num_iterations == 0:
            return pattern_3x3.num_cells_on
        if (
            pattern_3x3 in memoized_values
            and num_iterations in memoized_values[pattern_3x3]
        ):
            return memoized_values[pattern_3x3][num_iterations]
        new_pattern = pattern_3x3
        for _ in range(min(3, num_iterations)):
            new_pattern = self._run_iteration(new_pattern)

        if num_iterations < 3:
            result = new_pattern.num_cells_on
        else:
            result = sum(
                self._recursive_num_cells_for_3x3_blocks(
                    sub_block, num_iterations - 3, memoized_values
                )
                for sub_block in new_pattern.subdivide(3)
            )
        if pattern_3x3 not in memoized_values:
            memoized_values[pattern_3x3] = {}
        memoized_values[pattern_3x3][num_iterations] = result
        return result
