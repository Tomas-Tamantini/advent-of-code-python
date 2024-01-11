from input_output.file_parser import FileParser
from models.vectors import CardinalDirection
from models.aoc_2016 import Turtle, Keypad


parser = FileParser.default()


# AOC 2016 - Day 1: No Time for a Taxicab
def aoc_2016_d1(file_name: str):
    instructions = parser.parse_turtle_instructions(file_name)
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    for instruction in instructions:
        turtle.move(instruction)
    destination = turtle.position
    manhattan_distance = abs(destination.x) + abs(destination.y)
    print(
        f"AOC 2016 - Day 1/Part 1: Easter Bunny HQ is {manhattan_distance} blocks away"
    )
    self_intersection = next(turtle.path_self_intersections())
    manhattan_distance = abs(self_intersection.x) + abs(self_intersection.y)
    print(
        f"AOC 2016 - Day 1/Part 2: First point of self intersection is {manhattan_distance} blocks away"
    )


# AOC 2016 - Day 2: Bathroom Security
def aoc_2016_d2(file_name: str):
    keypad_three_by_three = Keypad(configuration="123\n456\n789", initial_key="5")
    keypad_rhombus = Keypad(
        configuration="**1**\n*234*\n56789\n*ABC*\n**D**", initial_key="5"
    )
    keys_3x3 = []
    keys_rhombus = []
    with open(file_name, "r") as f:
        for line in f.readlines():
            instructions = [
                FileParser.parse_cardinal_direction(i) for i in line.strip()
            ]
            keypad_three_by_three.move_multiple_keys(instructions)
            keys_3x3.append(keypad_three_by_three.key)
            keypad_rhombus.move_multiple_keys(instructions)
            keys_rhombus.append(keypad_rhombus.key)
    print(f"AOC 2016 - Day 2/Part 1: Bathroom code for 3x3 pad is {''.join(keys_3x3)}")
    print(
        f"AOC 2016 - Day 2/Part 2: Bathroom code for rhombus pad is {''.join(keys_rhombus)}"
    )
