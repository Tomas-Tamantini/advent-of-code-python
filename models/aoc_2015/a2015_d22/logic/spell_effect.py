from typing import Hashable, Iterator

from .characters import CharactersState


class SpellEffect:
    def __init__(
        self, id: Hashable, duration: int, is_high_priority: bool = False
    ) -> None:
        self._id = id
        self._duration = duration
        self._is_high_priority = is_high_priority

    def __str__(self) -> str:
        return f"{self._id} ({self._duration})"

    @property
    def id(self) -> Hashable:
        return self._id

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def is_high_priority(self) -> bool:
        return self._is_high_priority

    def apply(self, state: CharactersState) -> CharactersState:
        return state

    def wear_off(self, state: CharactersState) -> CharactersState:
        return state

    def __hash__(self) -> int:
        return hash(self._id)

    def __eq__(self, other) -> bool:
        return isinstance(other, SpellEffect) and self._id == other._id


class SpellEffectTimers:
    def __init__(self, timer: dict[SpellEffect, int]) -> None:
        self._timer = timer

    def add_spell_effect(self, effect: SpellEffect) -> "SpellEffectTimers":
        new_timer = {effect: time for effect, time in self._timer.items() if time > 0}
        if effect in new_timer:
            raise ValueError("Effect already active")
        new_timer[effect] = effect.duration
        return SpellEffectTimers(new_timer)

    def active_effects(self) -> Iterator[SpellEffect]:
        yield from (effect for effect, time in self._timer.items() if time > 0)

    def decrement_timers(self) -> "SpellEffectTimers":
        new_times = {effect: time - 1 for effect, time in self._timer.items()}
        return SpellEffectTimers(new_times)

    def effect_countdown(self, effect: SpellEffect) -> int:
        return self._timer.get(effect, 0)

    def wear_off_effects(self, state: CharactersState) -> CharactersState:
        characters = state
        for effect, countdown in self._timer.items():
            if countdown <= 0:
                characters = effect.wear_off(characters)
        return characters

    def __str__(self) -> str:
        return ", ".join(
            f"{effect} ({countdown})" for effect, countdown in self._timer.items()
        )

    def _effect_ids_with_times(self) -> Iterator[tuple[Hashable, int]]:
        yield from ((e.id, self._timer[e]) for e in self.active_effects())

    def __hash__(self) -> int:
        effects_with_times = list(self._effect_ids_with_times())
        return hash(tuple(sorted(effects_with_times)))

    def __eq__(self, other) -> bool:
        return isinstance(other, SpellEffectTimers) and tuple(
            self._effect_ids_with_times()
        ) == tuple(other._effect_ids_with_times())


class ShieldEffect(SpellEffect):
    def __init__(self, id: Hashable, duration: int, armor: int) -> None:
        super().__init__(id, duration)
        self._armor = armor

    def apply(self, state: CharactersState) -> CharactersState:
        new_wizard = state.wizard.add_armor(self._armor)
        return CharactersState(new_wizard, state.boss)

    def wear_off(self, state: CharactersState) -> CharactersState:
        new_wizard = state.wizard.remove_armor()
        return CharactersState(new_wizard, state.boss)


class PoisonEffect(SpellEffect):
    def __init__(self, id: Hashable, duration: int, damage: int) -> None:
        super().__init__(id, duration)
        self._damage = damage

    def apply(self, state: CharactersState) -> CharactersState:
        new_boss = state.boss.take_damage(self._damage)
        return CharactersState(state.wizard, new_boss)


class RechargeEffect(SpellEffect):
    def __init__(self, id: Hashable, duration: int, mana: int) -> None:
        super().__init__(id, duration)
        self._mana = mana

    def apply(self, state: CharactersState) -> CharactersState:
        new_wizard = state.wizard.recharge_mana(self._mana)
        return CharactersState(new_wizard, state.boss)


class DrainWizardHealthEffect(SpellEffect):
    def __init__(
        self,
        id: Hashable,
        duration: int,
        damage: int,
        is_high_priority: bool,
    ) -> None:
        super().__init__(id, duration, is_high_priority)
        self._damage = damage

    def apply(self, state: CharactersState) -> CharactersState:
        new_wizard = state.wizard.take_damage(self._damage, ignore_armor=True)
        return CharactersState(new_wizard, state.boss)
