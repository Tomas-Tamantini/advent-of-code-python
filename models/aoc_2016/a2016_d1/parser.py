from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import TurnDirection

from .turtle import TurtleInstruction


def parse_turtle_instructions(input_reader: InputReader) -> Iterator[TurtleInstruction]:
    text = input_reader.read()
    for instruction in text.split(","):
        stripped_instruction = instruction.strip()
        turn = TurnDirection(stripped_instruction[0])
        steps = int(stripped_instruction[1:])
        yield TurtleInstruction(turn, steps)
