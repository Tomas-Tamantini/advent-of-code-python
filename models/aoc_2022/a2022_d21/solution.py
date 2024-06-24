from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_operation_monkeys


def aoc_2022_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 21, "Monkey Math")
    io_handler.output_writer.write_header(problem_id)
    monkeys = parse_operation_monkeys(io_handler.input_reader)
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.evaluate()
    yield ProblemSolution(problem_id, f"Root monkey will yell {result}", part=1)

    monkeys = parse_operation_monkeys(
        io_handler.input_reader, monkey_with_unknown_value="humn"
    )
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.solve_for_equality()
    yield ProblemSolution(problem_id, f"You should yell {result}", part=2)
