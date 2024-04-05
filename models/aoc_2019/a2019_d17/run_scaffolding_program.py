from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program
from .scaffold_map import ScaffoldMap
from .vacuum_robot_io import CameraOutput


def run_scaffolding_discovery_program(
    scaffold_map: ScaffoldMap, instructions: list[int]
) -> None:
    program = IntcodeProgram(instructions[:])
    camera_output = CameraOutput(scaffold_map)
    run_intcode_program(program, serial_output=camera_output)
