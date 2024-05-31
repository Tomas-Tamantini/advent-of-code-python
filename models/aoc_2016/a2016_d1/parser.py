from typing import Iterator
from models.common.vectors import TurnDirection
from models.common.io import InputReader
from .turtle import TurtleInstruction


def parse_turtle_instructions(input_reader: InputReader) -> Iterator[TurtleInstruction]:
    text = input_reader.read()
    for instruction in text.split(","):
        instruction = instruction.strip()
        turn = TurnDirection(instruction[0])
        steps = int(instruction[1:])
        yield TurtleInstruction(turn, steps)
