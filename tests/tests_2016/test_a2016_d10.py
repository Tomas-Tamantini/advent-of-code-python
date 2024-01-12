import pytest
from models.aoc_2016.a2016_d10 import (
    ChipHandlerRobot,
    RobotInstruction,
    ChipAssignment,
    RobotProgramming,
    ChipFactory,
)


def _build_robot(
    instruction_low_id_chip: RobotInstruction = None,
    instruction_high_id_chip: RobotInstruction = None,
) -> ChipHandlerRobot:
    instruction_low_id_chip = instruction_low_id_chip or RobotInstruction(
        destination_id=1, goes_to_output_bin=True
    )
    instruction_high_id_chip = instruction_high_id_chip or RobotInstruction(
        destination_id=2, goes_to_output_bin=True
    )
    program = RobotProgramming(instruction_low_id_chip, instruction_high_id_chip)
    return ChipHandlerRobot(program)


def test_robot_starts_with_no_chips():
    robot = _build_robot()
    assert robot.num_chips == 0


def test_can_assign_chip_to_robot():
    robot = _build_robot()
    robot.assign_chip(chip_id=13)
    assert robot.num_chips == 1


def test_cannot_assign_more_than_two_chips_to_robot():
    robot = _build_robot()
    robot.assign_chip(chip_id=13)
    robot.assign_chip(chip_id=17)
    with pytest.raises(ValueError):
        robot.assign_chip(chip_id=19)


def test_robot_will_not_follow_instruction_if_it_does_not_have_enough_chips():
    instruction_low = RobotInstruction(destination_id=1, goes_to_output_bin=True)
    instruction_high = RobotInstruction(destination_id=2, goes_to_output_bin=True)
    robot = _build_robot(instruction_low, instruction_high)
    with pytest.raises(ValueError):
        _ = list(robot.chips_assignments())


def test_robot_will_follow_instructions_if_enough_chips():
    instruction_low = RobotInstruction(destination_id=1, goes_to_output_bin=True)
    instruction_high = RobotInstruction(destination_id=2, goes_to_output_bin=False)
    robot = _build_robot(instruction_low, instruction_high)
    robot.assign_chip(chip_id=13)
    robot.assign_chip(chip_id=17)
    assignments = list(robot.chips_assignments())
    assert len(assignments) == 2
    assert assignments == [
        ChipAssignment(chip_id=13, instruction=instruction_low),
        ChipAssignment(chip_id=17, instruction=instruction_high),
    ]


def test_factory_without_input_assignments_produces_no_chips():
    factory = ChipFactory(input_assignments=[], robot_programs=dict())
    factory.run()
    assert factory.output_bins == dict()


def _build_example_factory():
    input_assignments = [
        ChipAssignment(
            chip_id=5,
            instruction=RobotInstruction(destination_id=2),
        ),
        ChipAssignment(
            chip_id=3,
            instruction=RobotInstruction(destination_id=1),
        ),
        ChipAssignment(
            chip_id=2,
            instruction=RobotInstruction(destination_id=2),
        ),
    ]

    programs = {
        0: RobotProgramming(
            instruction_low_id_chip=RobotInstruction(
                destination_id=2, goes_to_output_bin=True
            ),
            instruction_high_id_chip=RobotInstruction(
                destination_id=0, goes_to_output_bin=True
            ),
        ),
        1: RobotProgramming(
            instruction_low_id_chip=RobotInstruction(
                destination_id=1, goes_to_output_bin=True
            ),
            instruction_high_id_chip=RobotInstruction(
                destination_id=0, goes_to_output_bin=False
            ),
        ),
        2: RobotProgramming(
            instruction_low_id_chip=RobotInstruction(
                destination_id=1, goes_to_output_bin=False
            ),
            instruction_high_id_chip=RobotInstruction(
                destination_id=0, goes_to_output_bin=False
            ),
        ),
    }

    return ChipFactory(input_assignments, programs)


def test_factory_programs_its_robots_and_produces_chips():
    factory = _build_example_factory()
    factory.run()
    assert factory.output_bins == {
        0: [5],
        1: [2],
        2: [3],
    }


def test_factory_keeps_track_of_what_robot_did_what():
    factory = _build_example_factory()
    factory.run()
    assert factory.robot_that_compared_chips(2, 5) == 2
    assert factory.robot_that_compared_chips(100, 200) == -1
