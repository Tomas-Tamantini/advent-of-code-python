from input_output.file_parser import FileParser
from models.aoc_2016 import turtle_destination

parser = FileParser.default()


# AOC 2016 - Day 1: No Time for a Taxicab
def aoc_2016_d1(file_name: str):
    instructions = parser.parse_turtle_instructions(file_name)
    destination = turtle_destination(instructions)
    manhattan_distance = abs(destination.x) + abs(destination.y)
    print(
        f"AOC 2016 - Day 1/Part 1: Easter Bunny HQ is {manhattan_distance} blocks away"
    )
    print("AOC 2016 - Day 1/Part 2: Not implemented")
