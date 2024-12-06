from typing import Protocol

from ..board_piece import BoardPiece


class Board(Protocol):
    def move_piece_forward(self, piece: BoardPiece) -> BoardPiece: ...
