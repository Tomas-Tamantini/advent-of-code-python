from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_luggage_rules


def aoc_2020_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 7, "Handy Haversacks")
    io_handler.output_writer.write_header(problem_id)
    rules = parse_luggage_rules(io_handler.input_reader)
    my_bag = "shiny gold"
    possible_colors = set(rules.possible_colors_of_outermost_bag(my_bag))
    solution = ProblemSolution(
        problem_id, f"{len(possible_colors)} possible outermost bag colors", part=1
    )
    io_handler.output_writer.write_solution(solution)
    num_inside = rules.number_of_bags_contained_inside(my_bag)
    solution = ProblemSolution(
        problem_id, f"{my_bag} contains {num_inside} bags", part=2
    )
    io_handler.output_writer.write_solution(solution)
