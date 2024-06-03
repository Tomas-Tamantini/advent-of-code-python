from models.common.io import InputFromString
from models.common.vectors import CardinalDirection
from ..parser import parse_submarine_navigation_instructions


def test_parse_navigation_instructions_for_submarine_without_aim():
    file_content = """
                   forward 10
                   up 3
                   down 7"""
    instructions = list(
        parse_submarine_navigation_instructions(
            InputFromString(file_content), submarine_has_aim=False
        )
    )
    assert len(instructions) == 3
    assert instructions[1].direction == CardinalDirection.NORTH
    assert instructions[2].distance == 7


def test_parse_navigation_instructions_for_submarine_with_aim():
    file_content = """
                   up 13
                   forward 10
                   down 7"""
    instructions = list(
        parse_submarine_navigation_instructions(
            InputFromString(file_content), submarine_has_aim=True
        )
    )
    assert len(instructions) == 3
    assert instructions[0].increment == -13
    assert instructions[1].distance == 10
    assert instructions[2].increment == 7
