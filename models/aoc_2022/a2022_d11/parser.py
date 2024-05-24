from typing import Iterator
from models.common.io import InputReader
from .monkey import Monkey, NextMonkeyIndexRule


def _parse_monkey(lines: list[str], boredom_worry_level_divisor: int) -> Monkey:
    transform_expression = lines[1].split("=")[-1].strip().replace("old", "w")
    next_monkey_index_rule = NextMonkeyIndexRule(
        *(int(lines[i].split()[-1]) for i in (2, 3, 4))
    )
    monkey = Monkey(
        worry_level_transformation=lambda w: eval(transform_expression),
        boredom_worry_level_divisor=boredom_worry_level_divisor,
        next_monkey_index_rule=next_monkey_index_rule,
    )
    for starting_item in map(int, lines[0].split(":")[1].split(",")):
        monkey.give_item(starting_item)
    return monkey


def parse_monkeys(
    input_reader: InputReader, boredom_worry_level_divisor: int
) -> Iterator[Monkey]:
    lines = list(input_reader.read_stripped_lines())
    for i, line in enumerate(lines):
        if "Monkey" in line:
            next_lines = lines[i + 1 : i + 6]
            yield _parse_monkey(next_lines, boredom_worry_level_divisor)
