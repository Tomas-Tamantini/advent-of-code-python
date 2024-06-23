from models.common.io import IOHandler, Problem
from .parser import parse_luggage_rules


def aoc_2020_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 7, "Handy Haversacks")
    io_handler.output_writer.write_header(problem_id)
    rules = parse_luggage_rules(io_handler.input_reader)
    my_bag = "shiny gold"
    possible_colors = set(rules.possible_colors_of_outermost_bag(my_bag))
    print(f"Part 1: {len(possible_colors)} possible outermost bag colors")
    num_inside = rules.number_of_bags_contained_inside(my_bag)
    print(f"Part 2: {my_bag} contains {num_inside} bags")
