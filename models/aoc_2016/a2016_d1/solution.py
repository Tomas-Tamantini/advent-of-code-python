from models.common.io import IOHandler, Problem
from models.common.vectors import CardinalDirection
from .parser import parse_turtle_instructions
from .turtle import Turtle


def aoc_2016_d1(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 1, "No Time for a Taxicab")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(parse_turtle_instructions(io_handler.input_reader))
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    for instruction in instructions:
        turtle.move(instruction)
    destination = turtle.position
    manhattan_distance = destination.manhattan_size
    print(f"Part 1: Easter Bunny HQ is {manhattan_distance} blocks away")
    self_intersection = next(turtle.path_self_intersections())
    manhattan_distance = self_intersection.manhattan_size
    print(
        f"Part 2: First point of self intersection is {manhattan_distance} blocks away"
    )
