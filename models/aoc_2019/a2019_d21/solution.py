from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import (
    run_spring_droid_program,
    SpringScriptInstruction,
    SpringScriptInstructionType,
    SpringDroidInput,
    SpringDroidOutput,
    BeginDroidCommand,
)


def _log_error(io_handler: IOHandler, droid_output: SpringDroidOutput, part: int):
    error_msg = f"Part {part}: Spring bot fell into a hole. Try a different springscript.\n{droid_output.render()}"
    io_handler.output_writer.log_error(error_msg)


def aoc_2019_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 21, "Springdroid Adventure")
    io_handler.output_writer.write_header(problem_id)
    intcode_instructions = [
        int(code) for code in io_handler.input_reader.read().split(",")
    ]
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.WALK
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        yield ProblemSolution(
            problem_id, f"Hull damage from walking on the hull is {hull_damage}", part=1
        )

    except ValueError:
        _log_error(io_handler, droid_output, part=1)
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "B", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "H", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.RUN
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        yield ProblemSolution(
            problem_id, f"Hull damage from running on the hull is {hull_damage}", part=2
        )

    except ValueError:
        _log_error(io_handler, droid_output, part=2)
