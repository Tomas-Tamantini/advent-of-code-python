from unittest.mock import Mock
from typing import Optional
import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import (
    TetrisGameState,
    TetrisPieceGenerator,
    TetrisPiece,
    WindGenerator,
    tower_height,
)


def _build_tetris_game_state(
    width: int = 7,
    tetris_piece_generator: Optional[TetrisPieceGenerator] = None,
    wind_generator: Optional[WindGenerator] = None,
) -> TetrisGameState:
    tetris_piece_generator = tetris_piece_generator or Mock()
    wind_generator = wind_generator or WindGenerator([CardinalDirection.EAST])
    return TetrisGameState(width, tetris_piece_generator, wind_generator)


def test_tetris_game_state_is_empty_by_default():
    game_state = _build_tetris_game_state()
    assert game_state.tower_height() == 0


def test_tetris_piece_gets_dropped_2_units_away_from_left_edge_and_3_units_above_max_height():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2)], offset=Vector2D(0, 0)
    )
    game_state = _build_tetris_game_state(tetris_piece_generator=tetris_piece_generator)
    _ = game_state.drop_next_piece()
    tetris_piece_generator.generate_next_piece.assert_called_with(
        bottom_left_corner=Vector2D(2, 4)
    )


def test_first_tetris_piece_drops_until_it_hits_the_floor():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2), Vector2D(2, 3), Vector2D(2, 4)], offset=Vector2D(0, 0)
    )
    game_state = _build_tetris_game_state(tetris_piece_generator=tetris_piece_generator)
    next_state = game_state.drop_next_piece()
    assert next_state.tower_height() == 3


def test_wind_drags_tetris_piece_sideways():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(2, 2)], offset=Vector2D(0, 0)
    )
    game_state = _build_tetris_game_state(
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=WindGenerator([CardinalDirection.EAST]),
    )
    next_state = game_state.drop_next_piece()
    assert set(next_state.exposed_blocks()) == {
        Vector2D(4, 1),
    }


def test_wind_does_not_move_tetris_piece_if_obstacle():
    tetris_piece_generator = Mock()
    tetris_piece_generator.generate_next_piece.return_value = TetrisPiece(
        shape=[Vector2D(5, 2)], offset=Vector2D(0, 0)
    )
    game_state = TetrisGameState(
        width=7,
        tetris_piece_generator=tetris_piece_generator,
        wind_generator=WindGenerator([CardinalDirection.EAST]),
    )
    next_state = game_state.drop_next_piece()
    assert set(next_state.exposed_blocks()) == {
        Vector2D(6, 1),
    }


def test_tetris_pieces_stack_on_top_of_each_other():
    game_state = _example_initial_game_state()
    for _ in range(10):
        game_state = game_state.drop_next_piece()
    assert game_state.tower_height() == 17


def test_tetris_game_stores_only_exposed_blocks():
    game_state = _example_initial_game_state()
    for _ in range(3):
        game_state = game_state.drop_next_piece()
    assert len(set(game_state.exposed_blocks())) == 9


@pytest.mark.parametrize(
    "num_pieces_to_drop, expected_height",
    [
        (2022, 3068),
        (1_000_000_000_000, 1_514_285_714_288),
    ],
)
def test_tetris_tower_height_is_calculated_efficiently(
    num_pieces_to_drop, expected_height
):
    game_state = _example_initial_game_state()
    assert tower_height(game_state, num_pieces_to_drop) == expected_height


def _example_initial_game_state():
    return TetrisGameState(
        width=7,
        tetris_piece_generator=_example_pieces_generator(),
        wind_generator=_example_wind_generator(),
    )


def _example_wind_generator():
    wind_pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    return WindGenerator(
        tuple(
            CardinalDirection.EAST if char == ">" else CardinalDirection.WEST
            for char in wind_pattern
        )
    )


def _example_pieces_generator():
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
