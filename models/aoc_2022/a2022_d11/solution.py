from models.common.io import InputReader
from .monkey import Monkeys
from .parser import parse_monkeys


def aoc_2022_d11(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 11: Monkey in the Middle ---")
    monkeys = tuple(parse_monkeys(input_reader))
    keep_away_monkeys = Monkeys(monkeys)
    for _ in range(20):
        keep_away_monkeys.play_round()
    max_num_inspections = sorted(keep_away_monkeys.num_inspections())[-2:]
    monkey_business = max_num_inspections[0] * max_num_inspections[1]
    print(f"Part 1: Monkey business is {monkey_business}")
