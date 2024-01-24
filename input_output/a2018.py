from itertools import combinations
from input_output.file_parser import FileParser
from input_output.progress_bar import ProgressBarConsole
from models.aoc_2018 import (
    first_frequency_to_be_reached_twice,
    contains_exactly_n_of_any_letter,
    differing_indices,
    FabricArea,
)

parser = FileParser.default()
progress_bar = ProgressBarConsole()


# AOC 2018 Day 1: Chronal Calibration
def aoc_2018_d1(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
    terms = [int(line) for line in lines]
    print(f"AOC 2018 Day 1/Part 1: Frequency at the end of one cycle: {sum(terms)}")
    first_duplicate_freq = first_frequency_to_be_reached_twice(terms)
    print(f"AOC 2018 Day 1/Part 2: First duplicate frequency: {first_duplicate_freq}")


# AOC 2018 Day 2: Inventory Management System
def aoc_2018_d2(file_name: str):
    with open(file_name) as file:
        lines = file.readlines()
    ids = [line.strip() for line in lines]
    exactly_two = sum(contains_exactly_n_of_any_letter(id, 2) for id in ids)
    exactly_three = sum(contains_exactly_n_of_any_letter(id, 3) for id in ids)
    print(f"AOC 2018 Day 2/Part 1: Checksum of ids is {exactly_two * exactly_three}")
    letters_in_common = ""
    for i, j in combinations(range(len(ids)), 2):
        differing = list(differing_indices(ids[i], ids[j]))
        if len(differing) == 1:
            letters_in_common = ids[i][: differing[0]] + ids[i][differing[0] + 1 :]
            break

    print(
        f"AOC 2018 Day 2/Part 2: Letters in common between ids are {letters_in_common}"
    )


# AOC 2018 Day 3: No Matter How You Slice It
def aoc_2018_d3(file_name: str):
    rectangles = parser.parse_fabric_rectangles(file_name)
    fabric_area = FabricArea()
    fabric_area.distribute(list(rectangles))
    conflicting_points = fabric_area.points_with_more_than_one_claim
    print(
        f"AOC 2018 Day 3/Part 1: Number of square inches with multiple claims: {len(conflicting_points)}"
    )
    id_without_overlap = fabric_area.rectangle_without_overlap.id
    print(
        f"AOC 2018 Day 3/Part 2: Id of rectangle without overlap: {id_without_overlap}"
    )


# AOC 2018 Day 4: Repose Record
def aoc_2018_d4(file_name: str):
    guards = list(parser.parse_guard_logs(file_name))
    guard_most_asleep = max(guards, key=lambda g: g.total_minutes_asleep)
    minute_most_asleep = guard_most_asleep.minute_most_likely_to_be_asleep()
    product = guard_most_asleep.id * minute_most_asleep
    print(f"AOC 2018 Day 4/Part 1: Guard most asleep has product {product}")


# AOC 2018 Day 5: Alchemical Reduction
def aoc_2018_d5(file_name: str):
    print("AOC 2018 Day 5/Part 1: Not Implemented")


# AOC 2018 Day 6: Chronal Coordinates
def aoc_2018_d6(file_name: str):
    print("AOC 2018 Day 6/Part 1: Not Implemented")


# AOC 2018 Day 7: The Sum of Its Parts
def aoc_2018_d7(file_name: str):
    print("AOC 2018 Day 7/Part 1: Not Implemented")


# AOC 2018 Day 8: Memory Maneuver
def aoc_2018_d8(file_name: str):
    print("AOC 2018 Day 8/Part 1: Not Implemented")


# AOC 2018 Day 9: Marble Mania
def aoc_2018_d9(file_name: str):
    print("AOC 2018 Day 9/Part 1: Not Implemented")


# AOC 2018 Day 10: The Stars Align
def aoc_2018_d10(file_name: str):
    print("AOC 2018 Day 10/Part 1: Not Implemented")


# AOC 2018 Day 11: Chronal Charge
def aoc_2018_d11(file_name: str):
    print("AOC 2018 Day 11/Part 1: Not Implemented")


# AOC 2018 Day 12: Subterranean Sustainability
def aoc_2018_d12(file_name: str):
    print("AOC 2018 Day 12/Part 1: Not Implemented")


# AOC 2018 Day 13: Mine Cart Madness
def aoc_2018_d13(file_name: str):
    print("AOC 2018 Day 13/Part 1: Not Implemented")


# AOC 2018 Day 14: Chocolate Charts
def aoc_2018_d14(file_name: str):
    print("AOC 2018 Day 14/Part 1: Not Implemented")


# AOC 2018 Day 15: Beverage Bandits
def aoc_2018_d15(file_name: str):
    print("AOC 2018 Day 15/Part 1: Not Implemented")


# AOC 2018 Day 16: Chronal Classification
def aoc_2018_d16(file_name: str):
    print("AOC 2018 Day 16/Part 1: Not Implemented")


# AOC 2018 Day 17: Reservoir Research
def aoc_2018_d17(file_name: str):
    print("AOC 2018 Day 17/Part 1: Not Implemented")


# AOC 2018 Day 18: Settlers of The North Pole
def aoc_2018_d18(file_name: str):
    print("AOC 2018 Day 18/Part 1: Not Implemented")


# AOC 2018 Day 19: Go With The Flow
def aoc_2018_d19(file_name: str):
    print("AOC 2018 Day 19/Part 1: Not Implemented")


# AOC 2018 Day 20: A Regular Map
def aoc_2018_d20(file_name: str):
    print("AOC 2018 Day 20/Part 1: Not Implemented")


# AOC 2018 Day 21: Chronal Conversion
def aoc_2018_d21(file_name: str):
    print("AOC 2018 Day 21/Part 1: Not Implemented")


# AOC 2018 Day 22: Mode Maze
def aoc_2018_d22(file_name: str):
    print("AOC 2018 Day 22/Part 1: Not Implemented")


# AOC 2018 Day 23: Experimental Emergency Teleportation
def aoc_2018_d23(file_name: str):
    print("AOC 2018 Day 23/Part 1: Not Implemented")


# AOC 2018 Day 24: Immune System Simulator 20XX
def aoc_2018_d24(file_name: str):
    print("AOC 2018 Day 24/Part 1: Not Implemented")


# AOC 2018 Day 25: Four-Dimensional Adventure
def aoc_2018_d25(file_name: str):
    print("AOC 2018 Day 25/Part 1: Not Implemented")
