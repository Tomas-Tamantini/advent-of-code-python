from models.common.vectors import Vector2D

from ..logic import TetrisPieceGenerator


def test_tetris_piece_generator_generates_piece_such_that_bottom_left_corner_is_at_given_position():
    generator = TetrisPieceGenerator(shapes=((Vector2D(15, 15), Vector2D(16, 14)),))
    piece = generator.generate_next_piece(bottom_left_corner=Vector2D(10, 30))
    assert set(piece.positions()) == {
        Vector2D(10, 31),
        Vector2D(11, 30),
    }


def test_tetris_piece_generator_loops_through_shapes_and_wraps_to_beginning_of_list():
    shape_a = (Vector2D(15, 15), Vector2D(16, 14))
    shape_b = (Vector2D(0, 0), Vector2D(1, 0), Vector2D(2, 0))
    generator = TetrisPieceGenerator(shapes=(shape_a, shape_b))
    pieces = []
    for _ in range(4):
        pieces.append(generator.generate_next_piece(bottom_left_corner=Vector2D(0, 0)))
        generator = generator.increment()
    shapes = [piece.shape for piece in pieces]
    assert shapes == [shape_a, shape_b, shape_a, shape_b]
