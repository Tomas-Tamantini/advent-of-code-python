from models.common.io import IOHandler, Problem
from models.common.vectors import TurnDirection
from .mine_carts import MineCarts


def aoc_2018_d13(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 13, "Mine Cart Madness")
    io_handler.output_writer.write_header(problem_id)
    mine_layout = io_handler.input_reader.read()
    intersection_sequence = [
        TurnDirection.LEFT,
        TurnDirection.NO_TURN,
        TurnDirection.RIGHT,
    ]
    mine_carts = MineCarts(mine_layout, intersection_sequence)
    collisions = list(mine_carts.collisions())
    print(f"Part 1: Position of first collision: {collisions[0].x},{collisions[0].y}")
    last_position = list(mine_carts.cart_positions)[0]
    print(f"Part 2: Position of last cart: {last_position.x},{last_position.y}")
