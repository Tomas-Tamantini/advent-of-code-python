from models.common.io import InputReader, ProgressBarConsole
from .sequence_generator import SequenceGenerator, SequenceMatchFinder


def aoc_2017_d15(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2017 - Day 15: Dueling Generators ---")
    start_a, start_b = [int(line.split()[-1]) for line in input_reader.readlines()]
    divisor = 2_147_483_647
    generator_a = SequenceGenerator(start_a, factor=16_807, divisor=divisor)
    generator_b = SequenceGenerator(start_b, factor=48_271, divisor=divisor)
    match_finder = SequenceMatchFinder(generator_a, generator_b, num_bits_to_match=16)
    num_matches = match_finder.num_matches(
        num_steps=40_000_000, progress_bar=progress_bar
    )
    print(f"Part 1: Number of matches not filtering out multiples: {num_matches}")
    generator_a.filter_multiples_of = 4
    generator_b.filter_multiples_of = 8
    num_matches = match_finder.num_matches(
        num_steps=5_000_000, progress_bar=progress_bar
    )
    print(f"Part 2: Number of matches filtering out multiples: {num_matches}")
