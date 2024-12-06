from typing import Optional

from .characters import Boss, Wizard
from .game_state import GameState
from .spell_effect import PoisonEffect, RechargeEffect, ShieldEffect, SpellEffect


class GameMove:
    def _new_wizard(self, game_state: GameState) -> Wizard:
        return game_state.wizard

    def _new_boss(self, game_state: GameState) -> Boss:
        return game_state.boss

    def _new_effect(self) -> Optional[SpellEffect]:
        return None

    def apply(self, game_state: GameState) -> GameState:
        new_state = GameState(
            wizard=self._new_wizard(game_state),
            boss=self._new_boss(game_state),
            is_wizard_turn=not game_state.is_wizard_turn,
            effect_timers=game_state.effect_timers,
        )
        effect = self._new_effect()
        if effect:
            return new_state.add_spell_effect(effect)
        else:
            return new_state


class Spell(GameMove):
    def __init__(self, mana_cost: int) -> None:
        super().__init__()
        self._mana_cost = mana_cost

    @property
    def mana_cost(self) -> int:
        return self._mana_cost

    def _new_wizard(self, game_state: GameState) -> Wizard:
        if game_state.wizard.mana < self._mana_cost:
            raise ValueError("Not enough mana")
        return game_state.wizard.spend_mana(self._mana_cost)


class BossMove(GameMove):
    def __init__(self, damage: int) -> None:
        super().__init__()
        self._damage = damage

    def _new_wizard(self, game_state: GameState) -> Wizard:
        return game_state.wizard.take_damage(self._damage)


class MagicMissile(Spell):
    def __init__(self, mana_cost: int, damage: int) -> None:
        self._mana_cost = mana_cost
        self._damage = damage

    def _new_boss(self, game_state: GameState) -> Boss:
        return game_state.boss.take_damage(self._damage)


class Drain(Spell):
    def __init__(self, mana_cost: int, damage: int, heal: int) -> None:
        super().__init__(mana_cost)
        self._damage = damage
        self._heal = heal

    def _new_wizard(self, game_state: GameState) -> Wizard:
        wizard_minus_mana = super()._new_wizard(game_state)
        return wizard_minus_mana.heal(self._heal)

    def _new_boss(self, game_state: GameState) -> Boss:
        return game_state.boss.take_damage(self._damage)


class Shield(Spell):
    def __init__(self, mana_cost: int, duration: int, armor: int) -> None:
        super().__init__(mana_cost)
        self._effect = ShieldEffect(id="shield", duration=duration, armor=armor)

    def _new_effect(self) -> Optional[SpellEffect]:
        return self._effect


class Poison(Spell):
    def __init__(self, mana_cost: int, duration: int, damage: int) -> None:
        super().__init__(mana_cost)
        self._effect = PoisonEffect(id="poison", duration=duration, damage=damage)

    def _new_effect(self) -> Optional[SpellEffect]:
        return self._effect


class Recharge(Spell):
    def __init__(self, mana_cost: int, duration: int, mana_recharge: int) -> None:
        super().__init__(mana_cost)
        self._effect = RechargeEffect(
            id="recharge", duration=duration, mana=mana_recharge
        )

    def _new_effect(self) -> Optional[SpellEffect]:
        return self._effect
