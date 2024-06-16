from models.common.io import InputReader
from models.common.vectors import CardinalDirection
from .parser import parse_cube_net_and_instructions
from .logic import BoardNavigator, PacmanEdgeMapper, CubeBoard


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
    cube_net, instructions = parse_cube_net_and_instructions(
        input_reader, edge_length=50
    )
    pacman_edge_mapper = PacmanEdgeMapper(cube_net)
    board = CubeBoard(pacman_edge_mapper)
    navigator = BoardNavigator(
        position=board.initial_position, facing=CardinalDirection.EAST
    )
    for instruction in instructions:
        navigator = instruction.execute(navigator, board)
    password = _navigator_password(navigator)
    print(f"Part 1: The password with pacman map is {password}")
