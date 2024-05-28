from models.common.io import InputReader
from .polymer_reaction import polymer_reaction, minimum_polymer_length


def aoc_2018_d5(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 5: Alchemical Reduction ---")
    polymer = input_reader.read().strip()
    reacted_polymer = polymer_reaction(polymer)
    print(f"Part 1: Length of reacted polymer: {len(reacted_polymer)}")
    min_length = minimum_polymer_length(polymer)
    print(f"Part 2: Minimum length of polymer: {min_length}")
