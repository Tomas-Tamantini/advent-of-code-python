from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program

from .springdroid_io import SpringDroidInput, SpringDroidOutput


def run_spring_droid_program(
    intcode_instructions: list[int],
    droid_input: SpringDroidInput,
    droid_output: SpringDroidOutput,
) -> None:
    intcode_program = IntcodeProgram(intcode_instructions[:])
    run_intcode_program(
        intcode_program, serial_input=droid_input, serial_output=droid_output
    )
