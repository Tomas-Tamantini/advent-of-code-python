from models.common.io import InputReader


def final_floor(instructions: str) -> int:
    return instructions.count("(") - instructions.count(")")


def first_basement(instructions: str) -> int:
    floor = 0
    for i, c in enumerate(instructions, 1):
        floor += 1 if c == "(" else -1
        if floor == -1:
            return i
    return -1


def aoc_2015_d1(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 1: Not Quite Lisp ---")
    instructions = input_reader.read()

    floor = final_floor(instructions)
    print(f"Part 1: Santa is on floor {floor}")

    basement = first_basement(instructions)
    print(f"Part 2: Santa first enters the basement at instruction {basement}")