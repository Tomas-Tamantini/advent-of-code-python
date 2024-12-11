from typing import Iterator


def _transform_stone(stone: int) -> Iterator[int]:
    if stone == 0:
        yield 1
    elif len((stone_str := str(stone))) % 2 == 0:
        half = len(stone_str) // 2
        yield int(stone_str[:half])
        yield int(stone_str[half:])
    else:
        yield stone * 2024


def transform_stones(stones: list[int]) -> Iterator[int]:
    for stone in stones:
        yield from _transform_stone(stone)
