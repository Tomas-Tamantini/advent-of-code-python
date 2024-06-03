from unittest.mock import Mock
from typing import Optional
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import TetrisChamber, TetrisPieceGenerator, TetrisPiece, WindGenerator


def _build_tetris_chamber(
    width: int = 7,
    tetris_piece_generator: Optional[TetrisPieceGenerator] = None,
    wind_generator: Optional[WindGenerator] = None,
) -> TetrisChamber:
    tetris_piece_generator = tetris_piece_generator or Mock()
    wind_generator = wind_generator or WindGenerator([CardinalDirection.EAST])
    return TetrisChamber(width, tetris_piece_generator, wind_generator)


def test_tetris_chamber_starts_empty():
    chamber = _build_tetris_chamber()
    assert chamber.max_height() == 0


def test_tetris_piece_gets_dropped_2_units_away_from_left_edge_and_3_units_above_max_height():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2)], offset=Vector2D(0, 0)
    )
    chamber = _build_tetris_chamber(tetris_piece_generator=tetris_piece_generator)
    chamber.drop_next_piece()
    tetris_piece_generator.generate_next_piece.assert_called_with(
        bottom_left_corner=Vector2D(2, 4)
    )


def test_first_tetris_piece_drops_until_hit_the_floor():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2), Vector2D(2, 3), Vector2D(2, 4)], offset=Vector2D(0, 0)
    )
    chamber = _build_tetris_chamber(tetris_piece_generator=tetris_piece_generator)
    chamber.drop_next_piece()
    assert chamber.max_height() == 3


def test_wind_drags_tetris_piece_sideways():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2)], offset=Vector2D(0, 0)
    )
    chamber = _build_tetris_chamber(
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=WindGenerator([CardinalDirection.EAST]),
    )
    chamber.drop_next_piece()
    assert set(chamber.settled_positions()) == {
        Vector2D(4, 1),
    }


def test_wind_does_not_move_tetris_piece_if_obstacle():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(5, 2)], offset=Vector2D(0, 0)
    )
    chamber = TetrisChamber(
        width=7,
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=WindGenerator([CardinalDirection.EAST]),
    )
    chamber.drop_next_piece()
    assert set(chamber.settled_positions()) == {
        Vector2D(6, 1),
    }


def test_tetris_pieces_stack_on_top_of_each_other():
    chamber = _build_tetris_chamber(
        width=7,
        tetris_piece_generator=_example_pieces_generator(),
        wind_generator=_example_wind_generator(),
    )
    for _ in range(10):
        chamber.drop_next_piece()
    assert chamber.max_height() == 17


def _example_wind_generator():
    wind_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    return WindGenerator(
        [
            CardinalDirection.EAST if char == ">" else CardinalDirection.WEST
            for char in wind_pattern
        ]
    )


def _example_pieces_generator():
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
