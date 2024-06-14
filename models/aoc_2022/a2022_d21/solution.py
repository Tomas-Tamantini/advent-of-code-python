from models.common.io import InputReader
from .parser import parse_operation_monkeys


def aoc_2022_d21(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 21: Monkey Math ---")
    monkeys = parse_operation_monkeys(input_reader)
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.evaluate()
    print(f"Part 1: Root monkey will yell {result}")

    monkeys = parse_operation_monkeys(input_reader, monkey_with_unknown_value="humn")
    root_monkey = next(m for m in monkeys if m.name == "root")
    result = root_monkey.solve_for_equality()
    print(f"Part 2: You should yell {result}")
