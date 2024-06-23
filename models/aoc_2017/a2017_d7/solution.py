from models.common.io import IOHandler
from .parser import parse_program_tree


def aoc_2017_d7(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2017 - Day 7: Recursive Circus ---")
    root = parse_program_tree(io_handler.input_reader)
    print(f"Part 1: Root node: {root.name}")
    imbalance = root.weight_imbalance()
    print(f"Part 2: Weight to fix imbalance: {imbalance.expected_weight}")
