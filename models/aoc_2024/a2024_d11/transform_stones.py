from typing import Iterator


def transform_stone(stone: int) -> Iterator[int]:
    if stone == 0:
        yield 1
    elif len((stone_str := str(stone))) % 2 == 0:
        half = len(stone_str) // 2
        yield int(stone_str[:half])
        yield int(stone_str[half:])
    else:
        yield stone * 2024


def num_transformed_stones(initial_stones: list[int], num_steps: int) -> int:
    memoized_results = {}
    return sum(
        _num_transformed_stones_recursive(s, num_steps, memoized_results)
        for s in initial_stones
    )


def _num_transformed_stones_recursive(
    stone: int, num_steps: int, memoized_results: dict[int, int]
) -> int:
    memoized_key = (stone, num_steps)
    if memoized_key in memoized_results:
        return memoized_results[memoized_key]
    elif num_steps == 0:
        return 1
    else:
        result = sum(
            _num_transformed_stones_recursive(
                new_stone, num_steps - 1, memoized_results
            )
            for new_stone in transform_stone(stone)
        )
        memoized_results[memoized_key] = result
        return result
