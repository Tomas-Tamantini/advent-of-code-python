from typing import Iterator
from models.common.io import InputReader
from .monkey import Monkey


def _parse_monkey(lines: list[str]) -> Monkey:
    transform_expression = lines[1].split("=")[-1].strip().replace("old", "w")
    test_div = int(lines[2].split()[-1])
    test_true = int(lines[3].split()[-1])
    test_false = int(lines[4].split()[-1])
    monkey = Monkey(
        worry_level_transformation=lambda w: eval(transform_expression),
        boredom_worry_level_divisor=3,
        next_monkey_index_rule=lambda w: (
            test_true if w % test_div == 0 else test_false
        ),
    )
    for starting_item in map(int, lines[0].split(":")[1].split(",")):
        monkey.give_item(starting_item)
    return monkey


def parse_monkeys(input_reader: InputReader) -> Iterator[Monkey]:
    lines = list(input_reader.read_stripped_lines())
    for i, line in enumerate(lines):
        if "Monkey" in line:
            next_lines = lines[i + 1 : i + 6]
            yield _parse_monkey(next_lines)
