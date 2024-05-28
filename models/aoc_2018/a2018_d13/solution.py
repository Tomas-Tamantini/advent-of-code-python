from models.common.io import InputReader
from models.common.vectors import TurnDirection
from .mine_carts import MineCarts


def aoc_2018_d13(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 13: Mine Cart Madness ---")
    mine_layout = input_reader.read()
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
