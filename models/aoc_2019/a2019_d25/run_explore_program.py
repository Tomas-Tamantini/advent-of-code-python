from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program
from .droid_input import DroidInput
from .droid_output import DroidOutput
from .droid_control import DroidCLIControl


def run_droid_explore_program(instructions: list[int]):
    intcode_program = IntcodeProgram(instructions[:])
    droid_input = DroidInput()
    control = DroidCLIControl(droid_input)
    droid_output = DroidOutput(output_handler=control)
    run_intcode_program(
        intcode_program, serial_input=droid_input, serial_output=droid_output
    )
