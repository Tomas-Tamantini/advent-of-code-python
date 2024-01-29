from dataclasses import dataclass
from models.vectors import CardinalDirection
from .units import CaveGameUnit
from .game_state import CaveGameState


class CaveGameMove:
    def _update_own_team(
        self,
        unit: CaveGameUnit,
        own_team: tuple[CaveGameUnit],
    ) -> tuple[CaveGameUnit]:
        return own_team

    def _update_opponent_team(
        self,
        unit: CaveGameUnit,
        opponent_team: tuple[CaveGameUnit],
    ) -> tuple[CaveGameUnit]:
        return opponent_team

    def execute(self, unit: CaveGameUnit, state: CaveGameState) -> CaveGameState:
        if unit in state.elves:
            return CaveGameState(
                elves=self._update_own_team(unit, state.elves),
                goblins=self._update_opponent_team(unit, state.goblins),
            )
        else:
            return CaveGameState(
                elves=self._update_opponent_team(unit, state.elves),
                goblins=self._update_own_team(unit, state.goblins),
            )


class MoveUnit(CaveGameMove):
    def __init__(self, direction: CardinalDirection) -> None:
        super().__init__()
        self._direction = direction

    @property
    def direction(self) -> CardinalDirection:
        return self._direction

    def _update_own_team(
        self,
        unit: CaveGameUnit,
        own_team: tuple[CaveGameUnit],
    ) -> tuple[CaveGameUnit]:
        return tuple(unit.move(self._direction) if c == unit else c for c in own_team)


class AttackMove(CaveGameMove):
    def __init__(self, target: CaveGameUnit) -> None:
        super().__init__()
        self._target = target

    @property
    def target(self) -> CaveGameUnit:
        return self._target

    def _update_opponent_team(
        self,
        unit: CaveGameUnit,
        opponent_team: tuple[CaveGameUnit],
    ) -> tuple[CaveGameUnit]:
        weakened_target = self._target.take_damage(unit.attack_power)
        if weakened_target.is_dead:
            return tuple(c for c in opponent_team if c != self._target)
        else:
            return tuple(
                self._target.take_damage(unit.attack_power) if c == self._target else c
                for c in opponent_team
            )
