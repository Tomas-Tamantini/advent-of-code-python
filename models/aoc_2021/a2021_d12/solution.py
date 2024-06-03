from models.common.io import InputReader
from .parser import parse_underwater_cave_connections
from .underwater_cave import UnderwaterCaveExplorer


def aoc_2021_d12(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 12: Passage Pathing ---")
    connections = parse_underwater_cave_connections(input_reader)
    explorer = UnderwaterCaveExplorer(
        connections, start_cave_name="start", end_cave_name="end"
    )
    paths = list(explorer.all_paths())
    print(f"Part 1: The number of paths from start to end is {len(paths)}")
    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    print(
        f"Part 2: The number of paths from start to end with one small cave visited twice is {len(paths)}"
    )