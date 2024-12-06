from typing import Iterator, Optional, Protocol

from .cave_map import CaveMap
from .game_moves import AttackMove, CaveGameMove, MoveUnit
from .game_state import CaveGameState
from .movement_maker import move_direction
from .units import CaveGameUnit


class CaveGameBot(Protocol):
    def bot_moves(
        self, unit: CaveGameUnit, game_state: CaveGameState, cave_map: CaveMap
    ) -> Iterator[CaveGameMove]: ...


class CaveGameBotAttackWeakest:
    def bot_moves(
        self, unit: CaveGameUnit, game_state: CaveGameState, cave_map: CaveMap
    ) -> Iterator[CaveGameMove]:
        weakest_opponent_in_range = self._weakest_opponent_in_range(unit, game_state)
        if weakest_opponent_in_range is None:
            direction = move_direction(unit, game_state, cave_map)
            if direction is not None:
                yield MoveUnit(direction=direction)
                new_unit = unit.move(direction)
                weakest_opponent_in_range = self._weakest_opponent_in_range(
                    new_unit, game_state
                )
        if weakest_opponent_in_range:
            yield AttackMove(target=weakest_opponent_in_range)

    @staticmethod
    def _weakest_opponent_in_range(
        unit: CaveGameUnit, game_state: CaveGameState
    ) -> Optional[CaveGameUnit]:
        weakest = None
        for opponent in game_state.adjacent_opponents(unit):
            if weakest is None or opponent.hit_points < weakest.hit_points:
                weakest = opponent
        return weakest
