from models.common.assembly import Processor, ImmutableProgram, Computer
from models.common.io import InputReader
from models.aoc_2018.three_value_instructions import ALL_THREE_VALUE_INSTRUCTIONS
from .parser import parse_instruction_samples, parse_unknown_op_code_program
from .unknown_op_code import possible_instructions, work_out_op_codes


def aoc_2018_d16(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 16: Chronal Classification ---")
    samples = list(parse_instruction_samples(input_reader))
    num_samples_with_three_or_more = sum(
        len(
            list(
                possible_instructions(
                    sample,
                    candidates=ALL_THREE_VALUE_INSTRUCTIONS,
                )
            )
        )
        >= 3
        for sample in samples
    )
    print(
        f"Part 1: Number of samples with three or more possible instructions: {num_samples_with_three_or_more}"
    )
    op_codes_to_instructions = work_out_op_codes(
        samples, candidates=ALL_THREE_VALUE_INSTRUCTIONS
    )
    instructions = parse_unknown_op_code_program(input_reader, op_codes_to_instructions)
    program = ImmutableProgram(list(instructions))
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    value = computer.get_register_value(register=0)
    print(f"Part 2: Value of register 0: {value}")
