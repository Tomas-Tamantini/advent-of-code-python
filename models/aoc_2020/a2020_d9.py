from typing import Iterator
from .a2020_d1 import subsets_that_sum_to


class XMasEncoding:
    def __init__(self, preamble_length: int) -> None:
        self._preamble_length = preamble_length

    def invalid_numbers(self, numbers: list[int]) -> Iterator[int]:
        for i in range(self._preamble_length, len(numbers)):
            target = numbers[i]
            preamble = numbers[i - self._preamble_length : i]
            subsets = list(subsets_that_sum_to(target, subset_size=2, entries=preamble))
            if not subsets:
                yield target

    @staticmethod
    def contiguous_numbers_which_sum_to_target(
        numbers: list[int], target: int
    ) -> Iterator[tuple[int, ...]]:
        if not numbers:
            return
        start_idx = 0
        end_idx = 1
        current_sum = sum(numbers[start_idx:end_idx])
        while start_idx < len(numbers):
            if current_sum == target:
                yield tuple(numbers[start_idx:end_idx])
                current_sum -= numbers[start_idx]
                start_idx += 1
                end_idx = max(start_idx + 1, end_idx)
            elif current_sum < target:
                if end_idx == len(numbers):
                    break
                current_sum += numbers[end_idx]
                end_idx += 1
            else:
                current_sum -= numbers[start_idx]
                start_idx += 1
