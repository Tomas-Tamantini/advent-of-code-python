from models.common.io import IOHandler, Problem
from .parser import parse_string_scrambler


def aoc_2016_d21(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 21, "Scrambled Letters and Hash")
    io_handler.output_writer.write_header(problem_id)
    scrambler = parse_string_scrambler(io_handler.input_reader)
    password = scrambler.scramble("abcdefgh")
    print(f"Part 1: Password after scrambling: {password}")
    password = scrambler.unscramble("fbgdceah")
    print(f"Part 2: Password before scrambling: {password}")
