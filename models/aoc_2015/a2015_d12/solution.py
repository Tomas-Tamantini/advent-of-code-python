from models.common.io import IOHandler, Problem, ProblemSolution
from .json_parser import sum_all_numbers_in_json


def aoc_2015_d12(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 12, "JSAbacusFramework.io")
    io_handler.output_writer.write_header(problem_id)
    json_str = io_handler.input_reader.read()
    json_sum = sum_all_numbers_in_json(json_str)
    solution = ProblemSolution(
        problem_id, f"Sum of all numbers in JSON is {json_sum}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    json_sum_minus_red = sum_all_numbers_in_json(json_str, property_to_ignore="red")
    solution = ProblemSolution(
        problem_id,
        f"Sum of all numbers in JSON ignoring 'red' property is {json_sum_minus_red}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
