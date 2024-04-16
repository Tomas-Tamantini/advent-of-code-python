from typing import Iterator
from itertools import product


class VectorNDimensional:
    def __init__(self, *coordinates: int) -> None:
        self._coordinates = coordinates

    @property
    def num_dimensions(self) -> int:
        return len(self._coordinates)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, VectorNDimensional):
            return False
        return self._coordinates == value._coordinates

    def __hash__(self) -> int:
        return hash(self._coordinates)

    def __iter__(self) -> Iterator[int]:
        yield from self._coordinates

    def __add__(self, other: "VectorNDimensional") -> "VectorNDimensional":
        return VectorNDimensional(*(a + b for a, b in zip(self, other)))

    def adjacent_positions(self) -> Iterator["VectorNDimensional"]:
        for deltas in product([-1, 0, 1], repeat=self.num_dimensions):
            if not any(deltas):
                continue
            yield VectorNDimensional(*(a + b for a, b in zip(self, deltas)))
