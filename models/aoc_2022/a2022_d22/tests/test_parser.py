from models.common.io import InputFromString
from models.common.vectors import TurnDirection, Vector2D

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
    parsed = parse_cube_net_and_instructions(InputFromString(input_str), edge_length=4)
    instructions = parsed.instructions
    assert len(instructions) == 13
    assert instructions[0].num_steps == 10
    assert instructions[1].turn_direction == TurnDirection.RIGHT

    walls = parsed.wall_positions
    assert len(walls) == 13
    assert Vector2D(3, 4) in walls

    assert parsed.cube_net.face_planar_positions == {
        Vector2D(2, 0),
        Vector2D(0, 1),
        Vector2D(1, 1),
        Vector2D(2, 1),
        Vector2D(2, 2),
        Vector2D(3, 2),
    }
