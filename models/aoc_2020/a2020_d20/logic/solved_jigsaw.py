from typing import Iterator
import numpy as np
from models.common.vectors import Vector2D, BoundingBox
from .jigsaw_piece import JigsawPiece
from .jigsaw_piece_orientation import JigsawPieceOrientation


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
            x = piece_width * position.x
            y = piece_height * (box.height - position.y)
            matrix[y : y + piece_height, x : x + piece_width] = (
                piece.render_without_border_details()
            )
        return matrix

    @staticmethod
    def _find_pattern_in_matrix(
        pattern: set[Vector2D], matrix: np.array
    ) -> Iterator[Vector2D]:
        for y in range(matrix.shape[0]):
            for x in range(matrix.shape[1]):
                all_positions_match = True
                for p in pattern:
                    if (
                        y + p.y >= matrix.shape[0]
                        or x + p.x >= matrix.shape[1]
                        or not matrix[y + p.y, x + p.x]
                    ):
                        all_positions_match = False
                        break
                if all_positions_match:
                    yield Vector2D(x, y)

    def find_pattern_matches(
        self, pattern: set[Vector2D]
    ) -> Iterator[tuple[Vector2D, JigsawPieceOrientation]]:
        matrix = self.render_as_matrix()
        for orientation in JigsawPieceOrientation.all_possible_orientations():
            oriented_matrix = orientation.transform(matrix)
            for matching_position in self._find_pattern_in_matrix(
                pattern, oriented_matrix
            ):
                yield matching_position, orientation
