import numpy as np
from input_output.file_parser import FileParser
from models.aoc_2017 import (
    digits_that_match_the_next,
    digits_that_match_one_across_the_circle,
    Spreadsheet,
    SquareSpiral,
)


parser = FileParser.default()


# AOC 2017 Day 1: Inverse Captcha
def aoc_2017_d1(file_name: str):
    with open(file_name) as f:
        digit_sequence = f.read().strip()
    sum_matches = sum(
        int(d) for d in digits_that_match_the_next(digit_sequence, wrap_around=True)
    )
    print(
        f"AOC 2017 Day 1/Part 1: Sum of digits that match the next one: {sum_matches}"
    )
    sum_matches = sum(
        int(d) for d in digits_that_match_one_across_the_circle(digit_sequence)
    )
    print(
        f"AOC 2017 Day 1/Part 2: Sum of digits that match one across the circle: {sum_matches}"
    )


# AOC 2017 Day 2: Corruption Checksum
def aoc_2017_d2(file_name: str):
    with open(file_name) as f:
        spreadsheet = Spreadsheet(np.loadtxt(f, dtype=int, delimiter="\t"))
    print(
        f"AOC 2017 Day 2/Part 1: Spreadsheet checksum min/max: {spreadsheet.checksum_min_max()}"
    )
    print(
        f"AOC 2017 Day 2/Part 2: Spreadsheet checksum divisibility: {spreadsheet.checksum_divisibility()}"
    )


# AOC 2017 Day 3: Spiral Memory
def aoc_2017_d3(file_name: str):
    with open(file_name) as f:
        target = int(f.read().strip())
    target_coordinates = SquareSpiral.coordinates(target)
    manhattan_distance = sum(abs(c) for c in target_coordinates)
    print(
        f"AOC 2017 Day 3/Part 1: Manhattan distance to {target}: {manhattan_distance}"
    )


# AOC 2017 Day 4: High-Entropy Passphrases
def aoc_2017_d4(file_name: str):
    print("AOC 2017 Day 4/Part 1: Not implemented")
    print("AOC 2017 Day 4/Part 2: Not implemented")


# AOC 2017 Day 5: A Maze of Twisty Trampolines, All Alike
def aoc_2017_d5(file_name: str):
    print("AOC 2017 Day 5/Part 1: Not implemented")
    print("AOC 2017 Day 5/Part 2: Not implemented")


# AOC 2017 Day 6: Memory Reallocation
def aoc_2017_d6(file_name: str):
    print("AOC 2017 Day 6/Part 1: Not implemented")
    print("AOC 2017 Day 6/Part 2: Not implemented")


# AOC 2017 Day 7: Recursive Circus
def aoc_2017_d7(file_name: str):
    print("AOC 2017 Day 7/Part 1: Not implemented")
    print("AOC 2017 Day 7/Part 2: Not implemented")


# AOC 2017 Day 8: I Heard You Like Registers
def aoc_2017_d8(file_name: str):
    print("AOC 2017 Day 8/Part 1: Not implemented")
    print("AOC 2017 Day 8/Part 2: Not implemented")


# AOC 2017 Day 9: Stream Processing
def aoc_2017_d9(file_name: str):
    print("AOC 2017 Day 9/Part 1: Not implemented")
    print("AOC 2017 Day 9/Part 2: Not implemented")


# AOC 2017 Day 10: Knot Hash
def aoc_2017_d10(file_name: str):
    print("AOC 2017 Day 10/Part 1: Not implemented")
    print("AOC 2017 Day 10/Part 2: Not implemented")


# AOC 2017 Day 11: Hex Ed
def aoc_2017_d11(file_name: str):
    print("AOC 2017 Day 11/Part 1: Not implemented")
    print("AOC 2017 Day 11/Part 2: Not implemented")


# AOC 2017 Day 12: Digital Plumber
def aoc_2017_d12(file_name: str):
    print("AOC 2017 Day 12/Part 1: Not implemented")
    print("AOC 2017 Day 12/Part 2: Not implemented")


# AOC 2017 Day 13: Packet Scanners
def aoc_2017_d13(file_name: str):
    print("AOC 2017 Day 13/Part 1: Not implemented")
    print("AOC 2017 Day 13/Part 2: Not implemented")


# AOC 2017 Day 14: Disk Defragmentation
def aoc_2017_d14(file_name: str):
    print("AOC 2017 Day 14/Part 1: Not implemented")
    print("AOC 2017 Day 14/Part 2: Not implemented")


# AOC 2017 Day 15: Dueling Generators
def aoc_2017_d15(file_name: str):
    print("AOC 2017 Day 15/Part 1: Not implemented")
    print("AOC 2017 Day 15/Part 2: Not implemented")


# AOC 2017 Day 16: Permutation Promenade
def aoc_2017_d16(file_name: str):
    print("AOC 2017 Day 16/Part 1: Not implemented")
    print("AOC 2017 Day 16/Part 2: Not implemented")


# AOC 2017 Day 17: Spinlock
def aoc_2017_d17(file_name: str):
    print("AOC 2017 Day 17/Part 1: Not implemented")
    print("AOC 2017 Day 17/Part 2: Not implemented")


# AOC 2017 Day 18: Duet
def aoc_2017_d18(file_name: str):
    print("AOC 2017 Day 18/Part 1: Not implemented")
    print("AOC 2017 Day 18/Part 2: Not implemented")


# AOC 2017 Day 19: A Series of Tubes
def aoc_2017_d19(file_name: str):
    print("AOC 2017 Day 19/Part 1: Not implemented")
    print("AOC 2017 Day 19/Part 2: Not implemented")


# AOC 2017 Day 20: Particle Swarm
def aoc_2017_d20(file_name: str):
    print("AOC 2017 Day 20/Part 1: Not implemented")
    print("AOC 2017 Day 20/Part 2: Not implemented")


# AOC 2017 Day 21: Fractal Art
def aoc_2017_d21(file_name: str):
    print("AOC 2017 Day 21/Part 1: Not implemented")
    print("AOC 2017 Day 21/Part 2: Not implemented")


# AOC 2017 Day 22: Sporifica Virus
def aoc_2017_d22(file_name: str):
    print("AOC 2017 Day 22/Part 1: Not implemented")
    print("AOC 2017 Day 22/Part 2: Not implemented")


# AOC 2017 Day 23: Coprocessor Conflagration
def aoc_2017_d23(file_name: str):
    print("AOC 2017 Day 23/Part 1: Not implemented")
    print("AOC 2017 Day 23/Part 2: Not implemented")


# AOC 2017 Day 24: Electromagnetic Moat
def aoc_2017_d24(file_name: str):
    print("AOC 2017 Day 24/Part 1: Not implemented")
    print("AOC 2017 Day 24/Part 2: Not implemented")


# AOC 2017 Day 25: The Halting Problem
def aoc_2017_d25(file_name: str):
    print("AOC 2017 Day 25: Not implemented")
