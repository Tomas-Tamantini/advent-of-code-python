from typing import Iterator


class AdapterArray:
    def __init__(
        self,
        outlet_joltage: int,
        device_joltage: int,
        max_joltage_difference: int,
        adapter_ratings: list[int],
    ) -> None:
        self._outlet_joltage = outlet_joltage
        self._device_joltage = device_joltage
        self._max_joltage_difference = max_joltage_difference
        self._adapter_ratings = adapter_ratings

    def joltage_differences_of_sorted_adapters(self) -> list[int]:
        sorted_joltages = sorted(self._adapter_ratings)
        sorted_joltages.insert(0, self._outlet_joltage)
        sorted_joltages.append(self._device_joltage)
        return [
            sorted_joltages[i] - sorted_joltages[i - 1]
            for i in range(1, len(sorted_joltages))
        ]

    def _split_into_segments(self, differences: list[int]) -> Iterator[list[int]]:
        current_segment = []
        for diff in differences:
            if diff == self._max_joltage_difference:
                if current_segment:
                    yield current_segment
                current_segment = []
            else:
                current_segment.append(diff)
        if current_segment:
            yield current_segment

    def _number_of_arrangements_recursive(
        self, differences: list[int], memoized: dict[tuple[int, ...], int]
    ) -> int:
        if len(differences) <= 1:
            return 1

        if tuple(differences) in memoized:
            return memoized[tuple(differences)]

        num_arrangements = 0

        # Case not remove adapter
        new_differences = differences[1:]
        num_arrangements += self._number_of_arrangements_recursive(
            new_differences, memoized
        )

        # Case remove adapter
        merged_sum = differences[0] + differences[1]
        if merged_sum < self._max_joltage_difference:
            new_differences = [merged_sum] + differences[2:]
            num_arrangements += self._number_of_arrangements_recursive(
                new_differences, memoized
            )
        elif merged_sum == self._max_joltage_difference:
            new_differences = differences[2:]
            num_arrangements += self._number_of_arrangements_recursive(
                new_differences, memoized
            )

        memoized[tuple(differences)] = num_arrangements
        return num_arrangements

    def number_of_arrangements(self) -> int:
        memoized = dict()
        differences = self.joltage_differences_of_sorted_adapters()
        product = 1
        for segment in self._split_into_segments(differences):
            product *= self._number_of_arrangements_recursive(segment, memoized)
        return product
