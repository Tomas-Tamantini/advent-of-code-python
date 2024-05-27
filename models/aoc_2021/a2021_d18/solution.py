from models.common.io import InputReader
from .snail_fish import SnailFishTree


def aoc_2021_d18(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 18: Snailfish ---")
    lines = list(input_reader.readlines())
    lists = [eval(line.strip()) for line in lines]
    acc = SnailFishTree.from_list(lists[0])
    for lst in lists[1:]:
        acc = acc + SnailFishTree.from_list(lst)
    print(f"Part 1: The magnitude of the snailfish is {acc.magnitude()}")

    largest_magnitude = 0
    for i in range(len(lists)):
        for j in range(len(lists)):
            if i != j:
                tree_i = SnailFishTree.from_list(lists[i])
                tree_j = SnailFishTree.from_list(lists[j])
                magnitude = (tree_i + tree_j).magnitude()
                if magnitude > largest_magnitude:
                    largest_magnitude = magnitude
    print(
        f"Part 2: The largest magnitude of the sum of two snailfish is {largest_magnitude}"
    )
