from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program
from .springscript_instruction import SpringScriptInstruction
from .springdroid_io import SpringDroidInput, SpringDroidOutput


def run_spring_droid_program(
    intcode_instructions: list[int],
    springscript_instructions: list[SpringScriptInstruction],
    output: SpringDroidOutput,
) -> None:
    intcode_program = IntcodeProgram(intcode_instructions[:])
    droid_input = SpringDroidInput(springscript_instructions)
    run_intcode_program(intcode_program, serial_input=droid_input, serial_output=output)
