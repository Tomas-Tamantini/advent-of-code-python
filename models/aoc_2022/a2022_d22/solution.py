from models.common.io import InputReader
from models.common.vectors import CardinalDirection, Vector2D
from .parser import parse_cube_net_and_instructions
from .logic import BoardPiece, PacmanEdgeMapper, CubeBoard, ObstacleBoard, CubeNet


def _initial_position(cube_net: CubeNet, cube_size: int) -> Vector2D:
    face_position = min(cube_net.face_planar_positions, key=lambda p: (p.y, p.x))
    return Vector2D(face_position.x * cube_size, face_position.y * cube_size)


def _build_password(board_piece: BoardPiece) -> int:
    row = board_piece.position.y + 1
    col = board_piece.position.x + 1
    facing_idx = {
        CardinalDirection.EAST: 0,
        CardinalDirection.SOUTH: 1,
        CardinalDirection.WEST: 2,
        CardinalDirection.NORTH: 3,
    }[board_piece.facing]
    return 1000 * row + 4 * col + facing_idx


def aoc_2022_d22(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 22: Monkey Map ---")
    cube_size = 50
    parsed = parse_cube_net_and_instructions(input_reader, cube_size)
    cube_net = parsed.cube_net
    initial_position = _initial_position(cube_net, cube_size)
    wall_positions = parsed.wall_positions
    pacman_edge_mapper = PacmanEdgeMapper(cube_net)
    cube_board = CubeBoard(cube_size, edge_mapper=pacman_edge_mapper)
    board = ObstacleBoard(cube_board, wall_positions)
    board_piece = BoardPiece(position=initial_position, facing=CardinalDirection.EAST)
    for instruction in parsed.instructions:
        board_piece = instruction.execute(board_piece, board)
    password = _build_password(board_piece)
    print(f"Part 1: The password with pacman map is {password}")
