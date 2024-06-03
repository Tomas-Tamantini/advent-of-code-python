from models.common.vectors import Vector2D, BoundingBox
from .tetris_piece import TetrisPiece


class TetrisPieceGenerator:
    def __init__(self, shapes: list[tuple[Vector2D, ...]]):
        self._shapes = shapes
        self._current_shape_index = 0

    def generate_next_piece(self, bottom_left_corner: Vector2D) -> TetrisPiece:
        shape = self._shapes[self._current_shape_index]
        self._current_shape_index = (self._current_shape_index + 1) % len(self._shapes)
        bounding_box = BoundingBox.from_points(shape)
        offset = bottom_left_corner - bounding_box.bottom_left
        return TetrisPiece(shape=shape, offset=offset)
