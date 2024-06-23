from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_interval_pairs


def aoc_2022_d4(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 4, "Camp Cleanup")
    io_handler.output_writer.write_header(problem_id)
    pairs = list(parse_interval_pairs(io_handler.input_reader))
    num_pairs_fully_contained = sum(
        interval_a.is_contained_by(interval_b) or interval_b.is_contained_by(interval_a)
        for interval_a, interval_b in pairs
    )
    solution = ProblemSolution(
        problem_id,
        f"Number of pairs in which one interval contains the other is {num_pairs_fully_contained}",
        part=1,
    )
    io_handler.set_solution(solution)

    num_pairs_with_overlap = sum(
        interval_a.intersection(interval_b) is not None
        for interval_a, interval_b in pairs
    )
    solution = ProblemSolution(
        problem_id,
        f"Number of pairs with some overlap {num_pairs_with_overlap}",
        part=2,
    )
    io_handler.set_solution(solution)
