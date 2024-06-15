from models.common.io import InputFromString
from models.common.vectors import Vector2D, TurnDirection, CardinalDirection
from ..logic import BoardNavigator
from ..parser import parse_obstacle_board_and_instructions


def test_parse_obstacle_board_and_instructions():
    input_str = "\n".join(
        (
            "        ...#    ",
            "        .#..    ",
            "        #...    ",
            "        ....    ",
            "...#.......#    ",
            "........#...    ",
            "..#....#....    ",
            "..........#.    ",
            "        ...#....",
            "        .....#..",
            "        .#......",
            "        ......#.",
            "                ",
            "10R5L5R10L4R5L5 ",
        )
    )
    board, instructions = parse_obstacle_board_and_instructions(
        InputFromString(input_str)
    )
    assert board.initial_position == Vector2D(8, 0)
    assert len(instructions) == 13
    assert instructions[0].num_steps == 10
    assert instructions[1].turn_direction == TurnDirection.RIGHT
    navigator = BoardNavigator(
        position=board.initial_position, facing=CardinalDirection.EAST
    )
    for instruction in instructions:
        navigator = instruction.execute(navigator, board)
    assert navigator.position == Vector2D(7, 5)
    assert navigator.facing == CardinalDirection.EAST
