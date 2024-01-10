from input_output.file_parser import FileParser, FileReader
from models.aoc_2016 import turtle_destination


def _get_file_name(day: int) -> str:
    return f"input_files/aoc_2016/a2016_d{day}.txt"


def _file_parser() -> FileParser:
    file_reader = FileReader()
    return FileParser(file_reader)


# AOC 2016 - Day 1: No Time for a Taxicab
def aoc_2016_d1():
    instructions = _file_parser().parse_turtle_instructions(_get_file_name(1))
    destination = turtle_destination(instructions)
    manhattan_distance = abs(destination.x) + abs(destination.y)
    print(
        f"AOC 2016 - Day 1/Part 1: Easter Bunny HQ is {manhattan_distance} blocks away"
    )
    print("AOC 2016 - Day 1/Part 2: Not implemented")


def advent_of_code_2016(*days: int):
    solutions = [aoc_2016_d1]
    if len(days) == 0:
        days = [i + 1 for i in range(len(solutions))]

    for day in days:
        solutions[day - 1]()
