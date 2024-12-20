from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .logic import TetrisGameState, TetrisPieceGenerator, WindGenerator, tower_height
from .parser import parse_wind_directions


def _pieces_generator() -> TetrisPieceGenerator:
    return TetrisPieceGenerator(
        shapes=(
            (
                Vector2D(0, 0),
                Vector2D(1, 0),
                Vector2D(2, 0),
                Vector2D(3, 0),
            ),
            (
                Vector2D(0, 1),
                Vector2D(1, 1),
                Vector2D(2, 1),
                Vector2D(1, 2),
                Vector2D(1, 0),
            ),
            (
                Vector2D(0, 0),
                Vector2D(1, 0),
                Vector2D(2, 0),
                Vector2D(2, 1),
                Vector2D(2, 2),
            ),
            (
                Vector2D(0, 0),
                Vector2D(0, 1),
                Vector2D(0, 2),
                Vector2D(0, 3),
            ),
            (
                Vector2D(0, 0),
                Vector2D(1, 0),
                Vector2D(0, 1),
                Vector2D(1, 1),
            ),
        )
    )


def aoc_2022_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 17, "Pyroclastic Flow")
    io_handler.output_writer.write_header(problem_id)
    wind_generator = WindGenerator(
        tuple(parse_wind_directions(io_handler.input_reader))
    )
    tetris_piece_generator = _pieces_generator()
    game_state = TetrisGameState(
        width=7,
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=wind_generator,
    )
    height = tower_height(game_state, 2022)
    yield ProblemSolution(
        problem_id,
        f"The height of the tower after 2022 rocks is {height}",
        part=1,
        result=height,
    )

    height = tower_height(game_state, 1_000_000_000_000)
    yield ProblemSolution(
        problem_id,
        f"The height of the tower after 1 trillion rocks is {height}",
        part=2,
        result=height,
    )
