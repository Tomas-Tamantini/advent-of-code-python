from models.common.io import InputReader
from .parser import parse_move_instructions
from .rope import Rope


def aoc_2022_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 9: Rope Bridge ---")
    rope = Rope()
    tail_positions = {rope.tail}
    for direction, distance in parse_move_instructions(input_reader):
        for _ in range(distance):
            rope = rope.move_head(direction)
            tail_positions.add(rope.tail)
    print(f"Part 1: Tail visited {len(tail_positions)} unique positions")
