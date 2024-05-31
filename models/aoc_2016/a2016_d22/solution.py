from models.common.io import InputReader
from .parser import parse_storage_nodes


def aoc_2016_d22(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 22: Grid Computing ---")
    nodes = list(parse_storage_nodes(input_reader))
    viable_pairs = sum(
        node_a.makes_viable_pair(node_b) for node_a in nodes for node_b in nodes
    )
    print(f"Part 1: Number of viable pairs: {viable_pairs}")
    print("Part 2: Done by hand (move hole around grid)")
