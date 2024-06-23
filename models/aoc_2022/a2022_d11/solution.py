from models.common.io import IOHandler, InputReader
from .monkey import Monkeys
from .parser import parse_monkeys


def _monkey_business(
    input_reader: InputReader, boredom_worry_level_divisor: int, num_rounds: int
) -> int:
    monkeys = tuple(parse_monkeys(input_reader, boredom_worry_level_divisor))
    keep_away_monkeys = Monkeys(monkeys)
    for _ in range(num_rounds):
        keep_away_monkeys.play_round()
    max_num_inspections = sorted(keep_away_monkeys.num_inspections())[-2:]
    return max_num_inspections[0] * max_num_inspections[1]


def aoc_2022_d11(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2022, 11, "Monkey in the Middle")
    monkey_business_20_rounds = _monkey_business(
        io_handler.input_reader, boredom_worry_level_divisor=3, num_rounds=20
    )
    print(f"Part 1: Monkey business for 20 rounds is {monkey_business_20_rounds}")
    monkey_business_10k_rounds = _monkey_business(
        io_handler.input_reader, boredom_worry_level_divisor=1, num_rounds=10_000
    )
    print(f"Part 2: Monkey business for 10,000 rounds is {monkey_business_10k_rounds}")
