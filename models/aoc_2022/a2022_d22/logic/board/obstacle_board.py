from models.common.vectors import Vector2D
from ..board_piece import BoardPiece
from .board import Board


class ObstacleBoard:
    def __init__(self, underlying_board: Board, wall_positions: set[Vector2D]) -> None:
        self._underlying_board = underlying_board
        self._wall_positions = wall_positions

    def move_piece_forward(self, piece: BoardPiece) -> BoardPiece:
        if (
            next_piece := self._underlying_board.move_piece_forward(piece)
        ).position in self._wall_positions:
            return piece
        else:
            return next_piece
