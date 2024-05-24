from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector2D, CardinalDirection
from .logic import Rope
from .parser import parse_move_instructions


def _tail_positions(
    rope: Rope, instructions: list[tuple[CardinalDirection, int]]
) -> Iterator[Vector2D]:
    yield rope.tail_position
    for direction, distance in instructions:
        for _ in range(distance):
            rope.move_head(direction)
            yield rope.tail_position


def aoc_2022_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 9: Rope Bridge ---")
    instructions = list(parse_move_instructions(input_reader))
    short_rope = Rope(num_knots=2)
    tail_positions = set(_tail_positions(short_rope, instructions))
    print(
        f"Part 1: Unique positions visited by tail in two-knot rope is {len(tail_positions)}"
    )
    long_rope = Rope(num_knots=10)
    tail_positions = set(_tail_positions(long_rope, instructions))
    print(
        f"Part 2: Unique positions visited by tail in ten-knot rope is {len(tail_positions)}"
    )
