from models.common.io import InputFromString
from models.common.vectors import Vector2D, TurnDirection, CardinalDirection
from ..logic import BoardNavigator, PacmanEdgeMapper, CubeBoard
from ..parser import parse_cube_net_and_instructions


def test_parse_obstacle_net_and_instructions():
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
    cube_net, instructions = parse_cube_net_and_instructions(
        InputFromString(input_str), edge_length=4
    )
    assert len(instructions) == 13
    assert instructions[0].num_steps == 10
    assert instructions[1].turn_direction == TurnDirection.RIGHT

    board = CubeBoard(edge_mapper=PacmanEdgeMapper(cube_net))
    assert board.initial_position == Vector2D(8, 0)
    navigator = BoardNavigator(
        position=board.initial_position, facing=CardinalDirection.EAST
    )
    for instruction in instructions:
        navigator = instruction.execute(navigator, board)
    assert navigator.position == Vector2D(7, 5)
    assert navigator.facing == CardinalDirection.EAST
