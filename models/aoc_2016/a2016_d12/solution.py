from models.common.io import InputReader
from models.common.assembly import Processor, Computer
from models.aoc_2016.assembunny import parse_assembunny_code


def aoc_2016_d12(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 12: Leonardo&apos;s Monorail ---")
    program = parse_assembunny_code(input_reader)
    program.optimize()
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    result_c_zero = computer.get_register_value("a")
    print(f"Part 1: Value of register a if c starts as 0: {result_c_zero}")
    computer = Computer.from_processor(Processor(registers={"c": 1}))
    computer.run_program(program)
    result_c_one = computer.get_register_value("a")
    print(f"Part 2: Value of register a if c starts as 1: {result_c_one}")
