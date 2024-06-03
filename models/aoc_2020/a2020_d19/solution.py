from models.common.io import InputReader
from .parser import parse_context_free_grammar_and_words


def aoc_2020_d19(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 19: Monster Messages ---")
    cfg, words = parse_context_free_grammar_and_words(input_reader, starting_symbol=0)
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 1: Number of valid messages is {num_matching}")

    cfg.add_rule(8, (42, 8))
    cfg.add_rule(11, (42, 11, 31))
    num_matching = sum(1 for word in words if cfg.matches(tuple(word)))
    print(f"Part 2: Number of valid messages with loops is {num_matching}")
