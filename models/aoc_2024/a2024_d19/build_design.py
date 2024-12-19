from typing import Iterable


def num_ways_to_make_design(design: str, available_patterns: Iterable[str]) -> int:
    memoized = dict()
    return _num_ways_recursive(design, available_patterns, memoized)


def _num_ways_recursive(
    design: str, available_patterns: Iterable[str], memoized: dict
) -> int:
    if not design:
        return 1
    if design not in memoized:
        memoized[design] = sum(
            _num_ways_recursive(design[len(pattern) :], available_patterns, memoized)
            for pattern in available_patterns
            if design.startswith(pattern)
        )
    return memoized[design]
