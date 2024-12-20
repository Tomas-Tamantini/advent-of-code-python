from typing import Iterator

from models.aoc_2018.three_value_instructions import ALL_THREE_VALUE_INSTRUCTIONS
from models.common.assembly import Computer, ImmutableProgram, Processor
from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_instruction_samples, parse_unknown_op_code_program
from .unknown_op_code import possible_instructions, work_out_op_codes


def aoc_2018_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 16, "Chronal Classification")
    io_handler.output_writer.write_header(problem_id)
    samples = list(parse_instruction_samples(io_handler.input_reader))
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
    yield ProblemSolution(
        problem_id,
        (
            "Number of samples with three or more possible instructions is "
            f"{num_samples_with_three_or_more}"
        ),
        result=num_samples_with_three_or_more,
        part=1,
    )

    op_codes_to_instructions = work_out_op_codes(
        samples, candidates=ALL_THREE_VALUE_INSTRUCTIONS
    )
    instructions = parse_unknown_op_code_program(
        io_handler.input_reader, op_codes_to_instructions
    )
    program = ImmutableProgram(list(instructions))
    computer = Computer.from_processor(Processor())
    computer.run_program(program)
    result = computer.get_register_value(register=0)
    yield ProblemSolution(problem_id, f"Value of register 0: {result}", result, part=2)
