from typing import Iterator
import numpy as np
from models.vectors import Vector2D, BoundingBox
from .jigsaw_piece import JigsawPiece


class SolvedJigsaw:
    def __init__(self, placed_pieces: dict[Vector2D, JigsawPiece]) -> None:
        self._placed_pieces = self._shifted_to_origin(placed_pieces)

    @staticmethod
    def _shifted_to_origin(
        placed_pieces: dict[Vector2D, JigsawPiece]
    ) -> dict[Vector2D, JigsawPiece]:
        bounding_box = BoundingBox.from_points(placed_pieces.keys())
        return {
            position - bounding_box.bottom_left: piece
            for position, piece in placed_pieces.items()
        }

    @property
    def placed_pieces(self) -> dict[Vector2D, JigsawPiece]:
        return self._placed_pieces

    def _bounding_box(self) -> BoundingBox:
        return BoundingBox.from_points(self._placed_pieces.keys())

    def border_pieces(self) -> Iterator[JigsawPiece]:
        box = self._bounding_box()
        yield self._placed_pieces[box.top_left]
        yield self._placed_pieces[box.top_right]
        yield self._placed_pieces[box.bottom_left]
        yield self._placed_pieces[box.bottom_right]

    def render_as_matrix(self) -> np.array:
        if not self._placed_pieces:
            return np.array([[]])
        sample_piece = next(iter(self._placed_pieces.values()))
        sample_piece_matrix = sample_piece.render_without_border_details()
        piece_width, piece_height = sample_piece_matrix.shape
        box = self._bounding_box()
        width = (box.width + 1) * piece_width
        height = (box.height + 1) * piece_height
        matrix = np.zeros((height, width), dtype=bool)
        for position, piece in self._placed_pieces.items():
            x = position.x * piece_width
            y = position.y * piece_height
            matrix[y : y + piece_height, x : x + piece_width] = (
                piece.render_without_border_details()
            )
        return matrix
