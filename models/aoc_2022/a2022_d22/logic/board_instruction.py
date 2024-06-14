from typing import Protocol
from dataclasses import dataclass
from models.common.vectors import TurnDirection
from .board_navigator import BoardNavigator
from .board import Board


class BoardInstruction(Protocol):
    def execute(self, navigator: BoardNavigator, board: Board) -> BoardNavigator: ...


@dataclass(frozen=True)
class TurnInstruction:
    turn_direction: TurnDirection

    def execute(self, navigator: BoardNavigator, board: Board) -> BoardNavigator:
        new_facing = navigator.facing.turn(self.turn_direction)
        return BoardNavigator(position=navigator.position, facing=new_facing)


@dataclass(frozen=True)
class MoveForwardInstruction:
    num_steps: int

    def execute(self, navigator: BoardNavigator, board: Board) -> BoardNavigator:
        new_position = board.next_position(navigator, self.num_steps)
        return BoardNavigator(position=new_position, facing=navigator.facing)
