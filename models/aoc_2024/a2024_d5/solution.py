from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import PageOrderingRules
from .parser import parse_page_ordering_rules, parse_updates


def aoc_2024_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 5, "Print Queue")
    io_handler.output_writer.write_header(problem_id)
    updates = list(parse_updates(io_handler.input_reader))
    rules = PageOrderingRules(list(parse_page_ordering_rules(io_handler.input_reader)))
    correct_updates = [u for u in updates if rules.is_in_correct_order(u)]
    total_correct = sum(u[len(u) // 2] for u in correct_updates)
    yield ProblemSolution(
        problem_id,
        f"The score from correctly ordered updates is {total_correct}",
        result=total_correct,
        part=1,
    )

    incorrect_updates = [u for u in updates if not rules.is_in_correct_order(u)]
    sorted_incorrect = [rules.sort_update(u) for u in incorrect_updates]
    total_incorrect = sum(u[len(u) // 2] for u in sorted_incorrect)
    yield ProblemSolution(
        problem_id,
        f"The score from incorrectly ordered updates is {total_incorrect}",
        result=total_incorrect,
        part=2,
    )
