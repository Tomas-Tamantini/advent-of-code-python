from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..fold_instruction import FoldInstruction
from ..parser import parse_positions_and_fold_instructions


def test_parse_positions_and_fold_instructions():
    file_content = """
                   2,14
                   8,10
                   9,0

                   fold along y=7
                   fold along x=5
                   """
    positions, instructions = parse_positions_and_fold_instructions(
        InputFromString(file_content)
    )
    assert positions == [Vector2D(2, 14), Vector2D(8, 10), Vector2D(9, 0)]
    assert instructions == [
        FoldInstruction(is_horizontal_fold=True, line=7),
        FoldInstruction(is_horizontal_fold=False, line=5),
    ]
