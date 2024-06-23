from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_form_answers_by_groups


def aoc_2020_d6(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 6, "Custom Customs")
    io_handler.output_writer.write_header(problem_id)
    groups = list(parse_form_answers_by_groups(io_handler.input_reader))
    union_yes = sum(len(group.questions_with_at_least_one_yes()) for group in groups)
    solution = ProblemSolution(
        problem_id, f"The sum of union 'yes' answers is {union_yes}", part=1
    )
    io_handler.set_solution(solution)

    intersection_yes = sum(
        len(group.questions_everyone_answered_yes()) for group in groups
    )
    solution = ProblemSolution(
        problem_id,
        f"The sum of intersection 'yes' answers is {intersection_yes}",
        part=2,
    )
    io_handler.set_solution(solution)
