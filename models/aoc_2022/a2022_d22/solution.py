from models.common.io import InputReader
from models.common.vectors import Vector2D, CardinalDirection
from .parser import parse_obstacle_board_and_instructions
from .logic import BoardNavigator


def _navigator_password(navigator: BoardNavigator) -> int:
    row = navigator.position.y + 1
    col = navigator.position.x + 1
    facing_idx = {
        CardinalDirection.EAST: 0,
        CardinalDirection.SOUTH: 1,
        CardinalDirection.WEST: 2,
        CardinalDirection.NORTH: 3,
    }[navigator.facing]
    return 1000 * row + 4 * col + facing_idx


def aoc_2022_d22(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 22: Monkey Map ---")
    board, instructions = parse_obstacle_board_and_instructions(input_reader)
    navigator = BoardNavigator(
        position=board.initial_position, facing=CardinalDirection.EAST
    )
    for instruction in instructions:
        navigator = instruction.execute(navigator, board)
    password = _navigator_password(navigator)
    print(f"Part 1: The password is {password}")
