from models.common.io import IOHandler, Problem, ProblemSolution
from .evaluate_expression import (
    evaluate_expression_addition_precedence,
    evaluate_expression_left_precedence,
)


def aoc_2020_d18(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 18, "Operation Order")
    io_handler.output_writer.write_header(problem_id)
    expressions = [line.strip() for line in io_handler.input_reader.readlines()]
    sum_results_left_precedence = sum(
        evaluate_expression_left_precedence(expression) for expression in expressions
    )
    solution = ProblemSolution(
        problem_id,
        f"Sum of results using left precedence is {sum_results_left_precedence}",
        part=1,
    )
    io_handler.set_solution(solution)

    sum_results_addition_precedence = sum(
        evaluate_expression_addition_precedence(expression)
        for expression in expressions
    )
    solution = ProblemSolution(
        problem_id,
        f"Sum of results using addition precedence is {sum_results_addition_precedence}",
        part=2,
    )
    io_handler.set_solution(solution)
