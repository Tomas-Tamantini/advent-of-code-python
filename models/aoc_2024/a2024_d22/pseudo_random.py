from typing import Iterator


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
