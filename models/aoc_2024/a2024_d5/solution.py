from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_page_ordering_rules, parse_updates
from .logic import PageOrderingRules


def aoc_2024_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 5, "Print Queue")
    io_handler.output_writer.write_header(problem_id)
    updates = list(parse_updates(io_handler.input_reader))
    rules = PageOrderingRules(list(parse_page_ordering_rules(io_handler.input_reader)))
    total = 0
    for update in updates:
        if rules.is_in_correct_order(update):
            mid_term = update[len(update) // 2]
            total += mid_term
    yield ProblemSolution(
        problem_id,
        f"The score from correctly ordered updates is {total}",
        result=total,
        part=1,
    )
