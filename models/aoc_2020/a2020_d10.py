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
