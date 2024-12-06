from dataclasses import dataclass
from typing import Protocol

from models.common.vectors import TurnDirection

from .board import Board
from .board_piece import BoardPiece


class BoardInstruction(Protocol):
    def execute(self, board_piece: BoardPiece, board: Board) -> BoardPiece: ...


@dataclass(frozen=True)
class TurnInstruction:
    turn_direction: TurnDirection

    def execute(self, board_piece: BoardPiece, board: Board) -> BoardPiece:
        return board_piece.turn(self.turn_direction)


@dataclass(frozen=True)
class MoveForwardInstruction:
    num_steps: int

    def execute(self, board_piece: BoardPiece, board: Board) -> BoardPiece:
        current_piece = board_piece
        for _ in range(self.num_steps):
            new_piece = board.move_piece_forward(current_piece)
            if new_piece == current_piece:
                break
            else:
                current_piece = new_piece
        return current_piece
