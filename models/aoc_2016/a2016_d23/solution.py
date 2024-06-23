from models.common.io import IOHandler
from models.aoc_2016.assembunny import parse_assembunny_code, run_self_referential_code


def aoc_2016_d23(io_handler: IOHandler) -> None:
    print("--- AOC 2016 - Day 23: Safe Cracking ---")
    program = parse_assembunny_code(io_handler.input_reader)
    a7 = run_self_referential_code(program, initial_value=7)
    print(f"Part 1: Value in register a if a starts as 7: {a7}")
    a12 = run_self_referential_code(program, initial_value=12)
    print(f"Part 2: Value in register a if a starts as 12: {a12}")
