from models.common.io import IOHandler, Problem
from .navigation_tree import parse_list_into_navigation_tree


def aoc_2018_d8(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 8, "Memory Maneuver")
    io_handler.output_writer.write_header(problem_id)
    numbers = list(map(int, io_handler.input_reader.read().split()))
    root = parse_list_into_navigation_tree(numbers)
    print(f"Part 1: Sum of metadata: {root.sum_of_metadata()}")
    print(f"Part 2: Value of root node: {root.navigation_value()}")
