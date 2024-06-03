from models.common.io import InputReader
from models.common.vectors import Vector2D
from .fold_instruction import FoldInstruction


def _parse_fold_instruction(line: str) -> FoldInstruction:
    is_horizontal = "y" in line
    index = int(line.split("=")[1])
    return FoldInstruction(is_horizontal, index)


def parse_positions_and_fold_instructions(
    input_reader: InputReader,
) -> tuple[list[Vector2D], list[FoldInstruction]]:
    positions = []
    instructions = []
    for line in input_reader.read_stripped_lines():
        if "fold" in line:
            instructions.append(_parse_fold_instruction(line))
        else:
            positions.append(Vector2D(*map(int, line.split(","))))
    return positions, instructions
