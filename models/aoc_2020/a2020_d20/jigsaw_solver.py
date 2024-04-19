from typing import Optional
from math import inf
from dataclasses import dataclass
from models.vectors import Vector2D, BoundingBox, CardinalDirection
from .jigsaw_piece_orientation import JigsawPieceOrientation
from .jigsaw_piece import JigsawPiece


@dataclass
class _JigsawBounds:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def contains(self, position: Vector2D) -> bool:
        return (
            self.min_x <= position.x <= self.max_x
            and self.min_y <= position.y <= self.max_y
        )


class JigsawSolver:
    def __init__(self) -> None:
        self._placed_pieces = dict()
        self._remaining_pieces = set()
        self._empty_positions = set()
        self._bounds = _JigsawBounds(min_x=-inf, max_x=inf, min_y=-inf, max_y=inf)

    def _reset(self):
        self._placed_pieces = dict()
        self._remaining_pieces = set()
        self._empty_positions = set()
        self._bounds = _JigsawBounds(min_x=-inf, max_x=inf, min_y=-inf, max_y=inf)

    def _update_bounds(self, out_of_bounds_position: Vector2D) -> None:
        neighbor_direction = next(
            direction
            for direction in CardinalDirection
            if out_of_bounds_position.move(direction) in self._placed_pieces
        )
        if neighbor_direction == CardinalDirection.NORTH:
            self._bounds.min_y = out_of_bounds_position.y + 1
        elif neighbor_direction == CardinalDirection.SOUTH:
            self._bounds.max_y = out_of_bounds_position.y - 1
        elif neighbor_direction == CardinalDirection.EAST:
            self._bounds.min_x = out_of_bounds_position.x + 1
        else:
            self._bounds.max_x = out_of_bounds_position.x - 1

    def _piece_fits(self, piece: JigsawPiece, position: Vector2D) -> bool:
        for orientation in JigsawPieceOrientation.all_possible_orientations():
            piece.reorient(orientation)
            for direction in CardinalDirection:
                adjacent_position = position.move(direction)
                if adjacent_position in self._placed_pieces:
                    neighboring_piece = self._placed_pieces[adjacent_position]
                    if not piece.can_place_other(neighboring_piece, direction):
                        return False
        return True

    def _next_piece_to_place(self, empty_position: Vector2D) -> Optional[JigsawPiece]:
        for piece in self._remaining_pieces:
            if self._piece_fits(piece, empty_position):
                return piece

    def _shift_back_to_origin(self) -> None:
        bounding_box = BoundingBox.from_points(self._placed_pieces.keys())
        new_placed_pieces = {
            position - bounding_box.bottom_left: piece
            for position, piece in self._placed_pieces.items()
        }
        self._placed_pieces = new_placed_pieces

    def _place_piece(self, piece: JigsawPiece, position: Vector2D) -> None:
        self._placed_pieces[position] = piece
        self._remaining_pieces.remove(piece)
        for adjacent_position in position.adjacent_positions():
            if adjacent_position not in self._placed_pieces:
                self._empty_positions.add(adjacent_position)

    def _try_fill_position(self, position: Vector2D) -> None:
        next_piece = self._next_piece_to_place(position)
        if next_piece is None:
            self._update_bounds(out_of_bounds_position=position)
        else:
            self._place_piece(next_piece, position)

    def solve_jigsaw(self, pieces: list[JigsawPiece]) -> dict[Vector2D, JigsawPiece]:
        self._reset()
        
        self._empty_positions.add(Vector2D(0, 0))
        self._remaining_pieces = set(pieces)

        while self._remaining_pieces:
            next_position = self._empty_positions.pop()
            if self._bounds.contains(next_position):
                self._try_fill_position(next_position)

        self._shift_back_to_origin()
        return self._placed_pieces
