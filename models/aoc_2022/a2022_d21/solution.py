from models.common.io import IOHandler, Problem
from .parser import parse_operation_monkeys


def aoc_2022_d21(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 21, "Monkey Math")
    io_handler.output_writer.write_header(problem_id)
    monkeys = parse_operation_monkeys(io_handler.input_reader)
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.evaluate()
    print(f"Part 1: Root monkey will yell {result}")

    monkeys = parse_operation_monkeys(
        io_handler.input_reader, monkey_with_unknown_value="humn"
    )
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.solve_for_equality()
    print(f"Part 2: You should yell {result}")
