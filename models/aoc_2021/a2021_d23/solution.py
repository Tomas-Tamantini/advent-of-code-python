from models.common.io import InputReader
from .parser import parse_amphipod_burrow
from .logic import AmphipodSorter


def aoc_2021_d23(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 23: Amphipod ---")
    burrow = parse_amphipod_burrow(input_reader)
    min_energy = AmphipodSorter().min_energy_to_sort(burrow)
    print(f"Part 1: The minimum energy to sort the burrow is {min_energy}")
    insertions = ("DD", "BC", "AB", "CA")
    extended_burrow = parse_amphipod_burrow(input_reader, *insertions)
    min_energy = AmphipodSorter().min_energy_to_sort(extended_burrow)
    print(f"Part 2: The minimum energy to sort the extended burrow is {min_energy}")