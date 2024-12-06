from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import CardinalDirection, Vector2D

from .logic import (
    BoardPiece,
    CubeBoard,
    CubeEdgeMapper,
    CubeNet,
    ObstacleBoard,
    PacmanEdgeMapper,
)
from .parser import parse_cube_net_and_instructions


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


def _simulate_movements(cube_size, edge_mapper, parsed_cube) -> BoardPiece:
    initial_position = _initial_position(parsed_cube.cube_net, cube_size)
    cube_board = CubeBoard(cube_size, edge_mapper)
    board = ObstacleBoard(cube_board, parsed_cube.wall_positions)
    board_piece = BoardPiece(position=initial_position, facing=CardinalDirection.EAST)
    for instruction in parsed_cube.instructions:
        board_piece = instruction.execute(board_piece, board)
    return _build_password(board_piece)


def aoc_2022_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 22, "Monkey Map")
    io_handler.output_writer.write_header(problem_id)

    cube_size = 50
    parsed = parse_cube_net_and_instructions(io_handler.input_reader, cube_size)

    pacman_edge_mapper = PacmanEdgeMapper(parsed.cube_net)
    password = _simulate_movements(cube_size, pacman_edge_mapper, parsed)
    yield ProblemSolution(
        problem_id,
        f"The password with pacman map is {password}",
        part=1,
        result=password,
    )

    cube_edge_mapper = CubeEdgeMapper(parsed.cube_net)
    password = _simulate_movements(cube_size, cube_edge_mapper, parsed)
    yield ProblemSolution(
        problem_id, f"The password with cube map is {password}", part=2, result=password
    )
