from collections import defaultdict
from typing import Iterable, Iterator


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


def maximize_winnings(seeds: Iterable[int], num_iterations: int) -> int:
    window_size = 4
    banana_count = defaultdict(int)
    for seed in seeds:
        sequence = tuple(n % 10 for n in pseudo_random_sequence(seed, num_iterations))
        differences = tuple((b - a) for a, b in zip(sequence, sequence[1:]))
        seen = set()
        for i in range(num_iterations + 1 - window_size):
            window = differences[i : i + window_size]
            if window not in seen:
                seen.add(window)
                banana_count[window] += sequence[i + window_size]
    return max(banana_count.values())
