from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .parser import parse_wind_directions
from .logic import WindGenerator, TetrisPieceGenerator, TetrisGameState, tower_height


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


def aoc_2022_d17(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2022 - Day 17: Pyroclastic Flow ---")
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
    print(f"Part 1: The height of the tower after 2022 rocks is {height}")
    height = tower_height(game_state, 1_000_000_000_000)
    print(f"Part 2: The height of the tower after 1 trillion rocks is {height}")
