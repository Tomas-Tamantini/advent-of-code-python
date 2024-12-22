from collections import defaultdict
from typing import Iterable, Iterator

from models.common.io import ProgressBar


def _next_pseudo_random(current: int) -> int:
    mod = 16777216
    current ^= current << 6
    current %= mod
    current ^= current >> 5
    current ^= current << 11
    current %= mod
    return current


def pseudo_random_sequence(seed: int, num_iterations: int) -> Iterator[int]:
    current = seed
    yield current
    for _ in range(num_iterations):
        current = _next_pseudo_random(current)
        yield current


def _prices_per_window(seed: int, num_iterations: int) -> dict[tuple[int, ...], int]:
    window_size = 4
    prices = dict()
    sequence = tuple(n % 10 for n in pseudo_random_sequence(seed, num_iterations))
    differences = tuple((b - a) for a, b in zip(sequence, sequence[1:]))
    for i in range(num_iterations + 1 - window_size):
        window = differences[i : i + window_size]
        if window not in prices:
            prices[window] = sequence[i + window_size]

    return prices


def maximize_winnings(
    seeds: Iterable[int], num_iterations: int, progress_bar: ProgressBar | None = None
) -> int:
    banana_count = defaultdict(int)
    for i, seed in enumerate(seeds):
        if progress_bar:
            progress_bar.update(i, len(seeds))
        for window, price in _prices_per_window(seed, num_iterations).items():
            banana_count[window] += price
    return max(banana_count.values())
