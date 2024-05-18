from models.common.vectors import Vector2D
from models.aoc_2021 import FoldInstruction


def test_folding_along_horizontal_line_transforms_y_coordinate_of_positions_below_fold_line():
    fold = FoldInstruction(is_horizontal_fold=True, line=7)
    positions = {Vector2D(19, 4), Vector2D(3, 9)}
    expected = {Vector2D(19, 4), Vector2D(3, 5)}
    assert fold.apply(positions) == expected


def test_folding_along_vertical_line_transforms_x_coordinate_of_positions_right_of_fold_line():
    fold = FoldInstruction(is_horizontal_fold=False, line=7)
    positions = {Vector2D(10, 24), Vector2D(3, 9)}
    expected = {Vector2D(4, 24), Vector2D(3, 9)}
    assert fold.apply(positions) == expected
