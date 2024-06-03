from typing import Iterator
from models.common.vectors import Vector2D, CardinalDirection
from .tetris_piece import TetrisPiece
from .tetris_piece_generator import TetrisPieceGenerator
from .wind_generator import WindGenerator


class TetrisChamber:
    def __init__(
        self,
        width: int,
        tetris_piece_generator: TetrisPieceGenerator,
        wind_generator: WindGenerator,
    ):
        self._piece_generator = tetris_piece_generator
        self._wind_generator = wind_generator
        self._settled_positions = set()
        self._max_height_by_column = [0] * width

    def max_height(self) -> int:
        return max(self._max_height_by_column)

    def settled_positions(self) -> Iterator[Vector2D]:
        return iter(self._settled_positions)

    def _drop_position(self) -> Vector2D:
        return Vector2D(2, self.max_height() + 4)

    def _collides_downwards(self, piece: TetrisPiece) -> bool:
        return any(
            pos.y <= self._max_height_by_column[pos.x] for pos in piece.positions()
        )

    def _is_out_of_bounds(self, pos: Vector2D) -> bool:
        return pos.x < 0 or pos.x >= len(self._max_height_by_column)

    def _collides(self, piece: TetrisPiece) -> bool:
        return any(self._is_out_of_bounds(pos) for pos in piece.positions()) or any(
            pos in self._settled_positions for pos in piece.positions()
        )

    def _settle_piece(self, piece: TetrisPiece) -> None:
        for pos in piece.positions():
            self._settled_positions.add(pos)
            self._max_height_by_column[pos.x] = max(
                self._max_height_by_column[pos.x], pos.y
            )

    def drop_next_piece(self) -> None:
        next_piece = self._piece_generator.generate_next_piece(
            bottom_left_corner=self._drop_position()
        )
        while True:
            wind_direction = self._wind_generator.next_wind_direction()
            candidate = next_piece.move(wind_direction)
            if not self._collides(candidate):
                next_piece = candidate
            candidate = next_piece.move(CardinalDirection.SOUTH)
            if not self._collides_downwards(candidate):
                next_piece = candidate
            else:
                self._settle_piece(next_piece)
                break
