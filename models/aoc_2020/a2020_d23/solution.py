from models.common.io import IOHandler, Problem, ProblemSolution
from .crab_cubs import crab_cups


def aoc_2020_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 23, "Crab Cups")
    io_handler.output_writer.write_header(problem_id)
    cups = [int(char) for char in io_handler.input_reader.read().strip()]
    result = crab_cups(cups, num_moves=100)
    one_index = result.index(1)
    result_str = "".join(
        str(num) for num in result[one_index + 1 :] + result[:one_index]
    )
    solution = ProblemSolution(
        problem_id, f"Cup labels after cup 1 are {result_str}", part=1
    )
    io_handler.set_solution(solution)
    cups += list(range(max(cups) + 1, 1_000_001))
    result = crab_cups(cups, num_moves=10_000_000, progress_bar=io_handler.progress_bar)
    one_index = result.index(1)
    result = result[one_index + 1 : one_index + 3]
    result_product = result[0] * result[1]
    solution = ProblemSolution(
        problem_id, f"Product of two cups after cup 1 is {result_product}", part=2
    )
    io_handler.set_solution(solution)
