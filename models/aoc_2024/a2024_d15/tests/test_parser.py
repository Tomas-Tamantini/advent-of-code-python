from models.common.io import InputFromString
from models.common.vectors import CardinalDirection, Vector2D

from ..parser import parse_warehouse, parse_warehouse_robot_moves

_FILE_CONTENT = """
                ########
                #..O.O.#
                ##@.O..#
                #...O..#
                #.#.O..#
                #...O..#
                #......#
                ########

                <^^>
                >v
                """


def test_parse_warehouse_robot_moves():
    input_reader = InputFromString(_FILE_CONTENT)
    moves = list(parse_warehouse_robot_moves(input_reader))
    assert moves == [
        CardinalDirection.WEST,
        CardinalDirection.NORTH,
        CardinalDirection.NORTH,
        CardinalDirection.EAST,
        CardinalDirection.EAST,
        CardinalDirection.SOUTH,
    ]


def test_parse_warehouse():
    warehouse = parse_warehouse(InputFromString(_FILE_CONTENT))
    assert warehouse.robot == Vector2D(2, 2)
    assert set(warehouse.box_positions()) == {
        Vector2D(4, 4),
        Vector2D(4, 3),
        Vector2D(3, 1),
        Vector2D(5, 1),
        Vector2D(4, 2),
        Vector2D(4, 5),
    }
    assert len(warehouse.walls) == 30
