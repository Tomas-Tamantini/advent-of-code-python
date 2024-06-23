from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_chip_factory


def aoc_2016_d10(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 10, "Balance Bots")
    io_handler.output_writer.write_header(problem_id)
    factory = parse_chip_factory(io_handler.input_reader)
    factory.run()
    bot_id = factory.robot_that_compared_chips(low_id=17, high_id=61)
    solution = ProblemSolution(
        problem_id, f"Bot that compared chips 17 and 61: {bot_id}", part=1
    )
    io_handler.set_solution(solution)
    chips_to_multiply = [factory.output_bins[i][0] for i in range(3)]
    product = chips_to_multiply[0] * chips_to_multiply[1] * chips_to_multiply[2]
    solution = ProblemSolution(
        problem_id, f"Product of chips in bins 0, 1, and 2: {product}", part=2
    )
    io_handler.set_solution(solution)
