from models.common.io import InputReader
from models.common.vectors import Vector2D
from .parser import parse_wind_directions
from .logic import WindGenerator, TetrisPieceGenerator, TetrisChamber


def _pieces_generator() -> TetrisPieceGenerator:
    return TetrisPieceGenerator(
        shapes=[
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
        ]
    )


def aoc_2022_d17(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 17: Pyroclastic Flow ---")
    wind_generator = WindGenerator(list(parse_wind_directions(input_reader)))
    tetris_piece_generator = _pieces_generator()
    tetris_chamber = TetrisChamber(
        width=7,
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=wind_generator,
    )
    for _ in range(2022):
        tetris_chamber.drop_next_piece()
    print(
        f"Part 1: The height of the tower after 2022 rocks is {tetris_chamber.tower_height()}"
    )
