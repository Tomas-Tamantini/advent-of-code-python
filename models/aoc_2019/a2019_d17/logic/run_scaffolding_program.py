from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program

from .path_compression import CompressedPath
from .scaffold_map import ScaffoldMap
from .vacuum_robot_io import CameraOutput, VacuumRobotInput, VacuumRobotOutput


def run_scaffolding_discovery_program(
    scaffold_map: ScaffoldMap, instructions: list[int]
) -> None:
    program = IntcodeProgram(instructions[:])
    camera_output = CameraOutput(scaffold_map)
    run_intcode_program(program, serial_output=camera_output)


def run_scaffolding_exploration_program(
    instructions: list[int],
    compressed_path: CompressedPath,
    watch_video_feed: bool = False,
) -> int:
    program = IntcodeProgram(instructions[:])
    vacuum_input = VacuumRobotInput(compressed_path, watch_video_feed)
    vacuum_output = VacuumRobotOutput()
    run_intcode_program(program, serial_input=vacuum_input, serial_output=vacuum_output)
    return vacuum_output.output_value
