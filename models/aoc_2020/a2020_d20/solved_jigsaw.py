from typing import Iterator
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
