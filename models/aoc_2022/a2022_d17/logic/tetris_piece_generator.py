from dataclasses import dataclass

from models.common.vectors import BoundingBox, Vector2D

from .tetris_piece import TetrisPiece


@dataclass(frozen=True)
class TetrisPieceGenerator:
    shapes: tuple[tuple[Vector2D, ...]]
    current_shape_index: int = 0

    def increment(self) -> "TetrisPieceGenerator":
        return TetrisPieceGenerator(
            shapes=self.shapes,
            current_shape_index=(self.current_shape_index + 1) % len(self.shapes),
        )

    def generate_next_piece(self, bottom_left_corner: Vector2D) -> TetrisPiece:
        shape = self.shapes[self.current_shape_index]
        bounding_box = BoundingBox.from_points(shape)
        offset = bottom_left_corner - bounding_box.bottom_left
        return TetrisPiece(shape=shape, offset=offset)
