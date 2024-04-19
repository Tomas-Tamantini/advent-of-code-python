from models.vectors import Vector2D, BoundingBox
from .jigsaw_piece import JigsawPiece


class SolvedJigsaw:
    def __init__(self, placed_pieces: dict[Vector2D, JigsawPiece]) -> None:
        bounding_box = BoundingBox.from_points(placed_pieces.keys())
        self._placed_pieces = {
            position - bounding_box.bottom_left: piece
            for position, piece in placed_pieces.items()
        }

    @property
    def placed_pieces(self) -> dict[Vector2D, JigsawPiece]:
        return self._placed_pieces
