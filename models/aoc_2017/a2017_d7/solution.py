from models.common.io import InputReader
from .parser import parse_program_tree


def aoc_2017_d7(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 7: Recursive Circus ---")
    root = parse_program_tree(input_reader)
    print(f"Part 1: Root node: {root.name}")
    imbalance = root.weight_imbalance()
    print(f"Part 2: Weight to fix imbalance: {imbalance.expected_weight}")
