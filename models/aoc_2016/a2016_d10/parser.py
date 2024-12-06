from models.common.io import InputReader

from .chip_factory import (
    ChipAssignment,
    ChipFactory,
    RobotInstruction,
    RobotProgramming,
)


def _parse_input_assignment(line: str) -> ChipAssignment:
    parts = line.strip().split(" ")
    return ChipAssignment(
        chip_id=int(parts[1]),
        instruction=RobotInstruction(destination_id=int(parts[-1])),
    )


def _parse_robot_program(line: str) -> tuple[int, RobotProgramming]:
    parts = line.strip().split(" ")
    robot_id = int(parts[1])
    destination_low = int(parts[-6])
    destination_high = int(parts[-1])
    low_is_output_bin = "output" in parts[5]
    high_is_output_bin = "output" in parts[-2]
    return robot_id, RobotProgramming(
        instruction_low_id_chip=RobotInstruction(
            destination_id=destination_low,
            goes_to_output_bin=low_is_output_bin,
        ),
        instruction_high_id_chip=RobotInstruction(
            destination_id=destination_high,
            goes_to_output_bin=high_is_output_bin,
        ),
    )


def parse_chip_factory(input_reader: InputReader) -> ChipFactory:
    input_assignments = list()
    robot_programs = dict()
    for line in input_reader.readlines():
        if "value" in line:
            input_assignments.append(_parse_input_assignment(line))
        else:
            robot_id, robot_program = _parse_robot_program(line)
            if robot_id in robot_programs:
                raise ValueError(f"Robot {robot_id} already has a program")
            robot_programs[robot_id] = robot_program
    return ChipFactory(input_assignments, robot_programs)
