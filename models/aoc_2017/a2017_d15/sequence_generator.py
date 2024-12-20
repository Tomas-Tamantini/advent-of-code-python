from dataclasses import dataclass
from typing import Iterator, Optional

from models.common.io import ProgressBar


@dataclass
class SequenceGenerator:
    starting_number: int
    factor: int
    divisor: int
    filter_multiples_of: int = 1

    def generate(self) -> Iterator[int]:
        next_num = self.starting_number
        while True:
            next_num = (next_num * self.factor) % self.divisor
            if next_num % self.filter_multiples_of == 0:
                yield next_num


class SequenceMatchFinder:
    def __init__(
        self,
        generator_a: SequenceGenerator,
        generator_b: SequenceGenerator,
        num_bits_to_match: int,
    ) -> None:
        self._generator_a = generator_a
        self._generator_b = generator_b
        self._mask = 2**num_bits_to_match - 1

    def _bits_match(self, a: int, b: int) -> bool:
        return a & self._mask == b & self._mask

    def num_matches(
        self, num_steps: int, progress_bar: Optional[ProgressBar] = None
    ) -> int:
        num_matches = 0
        a_generator = self._generator_a.generate()
        b_generator = self._generator_b.generate()
        for step in range(num_steps):
            if progress_bar:
                progress_bar.update(step, num_steps)
            next_a = next(a_generator)
            next_b = next(b_generator)
            if self._bits_match(next_a, next_b):
                num_matches += 1
        return num_matches
