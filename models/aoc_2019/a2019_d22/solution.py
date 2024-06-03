from models.common.io import InputReader
from .parser import parse_multi_technique_shuffle


def aoc_2019_d22(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 22: Slam Shuffle ---")
    shuffle = parse_multi_technique_shuffle(input_reader)
    new_position = shuffle.new_card_position(
        position_before_shuffle=2019, deck_size=10_007
    )
    print(f"Part 1: New position of card 2019 is {new_position}")
    original_position = shuffle.original_card_position(
        position_after_shuffle=2020,
        deck_size=119315717514047,
        num_shuffles=101741582076661,
    )
    print(f"Part 2: Original position of card 2020 is {original_position}")