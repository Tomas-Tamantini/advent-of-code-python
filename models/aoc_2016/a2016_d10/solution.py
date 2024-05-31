from models.common.io import InputReader
from .parser import parse_chip_factory


def aoc_2016_d10(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 10: Balance Bots ---")
    factory = parse_chip_factory(input_reader)
    factory.run()
    bot_id = factory.robot_that_compared_chips(low_id=17, high_id=61)
    print(f"Part 1: Bot that compared chips 17 and 61: {bot_id}")
    chips_to_multiply = [factory.output_bins[i][0] for i in range(3)]
    product = chips_to_multiply[0] * chips_to_multiply[1] * chips_to_multiply[2]
    print(f"Part 2: Product of chips in bins 0, 1, and 2: {product}")
