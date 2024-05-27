# See derivation at: https://colab.research.google.com/drive/1Lcx-KNL9YsY_IEIAdz7vBhqd-tpxWvju?usp=sharing
from typing import Callable


def _median(lst: list[int]) -> int:
    return sorted(lst)[len(lst) // 2]


def _mean(lst: list[int]) -> int:
    return sum(lst) // len(lst)


def _triangular_number(n: int) -> int:
    return n * (n + 1) // 2


def _total_fuel_consumption(
    positions: list[int], station: int, fuel_func: Callable[[int], int]
) -> int:
    return sum(fuel_func(abs(number - station)) for number in positions)


def optimal_linear_fuel_consumption(positions: list[int]) -> int:
    median_number = _median(positions)
    return _total_fuel_consumption(positions, median_number, lambda x: x)


def optimal_triangular_fuel_consumption(positions: list[int]) -> int:
    avg = _mean(positions)
    return min(
        _total_fuel_consumption(positions, candidate, _triangular_number)
        for candidate in range(avg - 2, avg + 3)
    )
