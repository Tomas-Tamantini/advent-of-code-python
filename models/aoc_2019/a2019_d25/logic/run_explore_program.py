from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program

from .droid_control import DroidControl
from .droid_output import DroidOutput


def run_droid_explore_program(instructions: list[int], control: DroidControl):
    intcode_program = IntcodeProgram(instructions[:])
    droid_output = DroidOutput(output_handler=control)
    run_intcode_program(
        intcode_program, serial_input=control.droid_input, serial_output=droid_output
    )
