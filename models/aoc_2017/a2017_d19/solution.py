from models.common.io import InputReader
from .package_router import PackageRouter


def aoc_2017_d19(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 19: A Series of Tubes ---")
    maze = [line for line in input_reader.readlines()]
    router = PackageRouter(maze)
    router.explore()
    print(f"Part 1: Letters visited: {''.join(router.visited_letters)}")
    print(f"Part 2: Number of routing steps: {router.num_steps}")
