from models.common.io import InputFromString
from models.common.vectors import TurnDirection

from ..parser import parse_turtle_instructions
from ..turtle import TurtleInstruction


def test_parse_turtle_instructions():
    instructions = list(parse_turtle_instructions(InputFromString("R2, L3")))
    assert instructions == [
        TurtleInstruction(TurnDirection.RIGHT, 2),
        TurtleInstruction(TurnDirection.LEFT, 3),
    ]
