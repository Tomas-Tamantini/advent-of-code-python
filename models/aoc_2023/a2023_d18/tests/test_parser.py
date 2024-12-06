from models.common.io import InputFromString
from models.common.vectors import CardinalDirection

from ..dig_plan import DiggerInstruction
from ..parser import parse_dig_plan


def test_parsing_dig_plan_ignoring_hexadecimal_considers_first_part_of_instructions():
    file_content = """R 6 (#70c710)
                      D 5 (#0dc571)
                      L 2 (#5713f0)
                      U 2 (#d2c081)"""
    input_reader = InputFromString(file_content)
    instructions = list(parse_dig_plan(input_reader, parse_hexadecimal=False))
    assert instructions == [
        DiggerInstruction(CardinalDirection.EAST, 6),
        DiggerInstruction(CardinalDirection.SOUTH, 5),
        DiggerInstruction(CardinalDirection.WEST, 2),
        DiggerInstruction(CardinalDirection.NORTH, 2),
    ]


def test_parsing_dig_plan_considering_hexadecimal_parses_direction_and_number_of_steps_from_hexadecimal():
    file_content = """R 6 (#70c710)
                      D 5 (#0dc571)
                      L 2 (#8ceee2)
                      U 2 (#caa173)"""
    input_reader = InputFromString(file_content)
    instructions = list(parse_dig_plan(input_reader, parse_hexadecimal=True))
    assert instructions == [
        DiggerInstruction(CardinalDirection.EAST, 461937),
        DiggerInstruction(CardinalDirection.SOUTH, 56407),
        DiggerInstruction(CardinalDirection.WEST, 577262),
        DiggerInstruction(CardinalDirection.NORTH, 829975),
    ]
