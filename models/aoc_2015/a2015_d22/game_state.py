from .characters import Boss, Wizard, CharactersState
from .spell_effect import SpellEffect, SpellEffectTimers


class GameState:
    def __init__(
        self,
        wizard: Wizard,
        boss: Boss,
        is_wizard_turn: bool,
        effect_timers: SpellEffectTimers = None,
    ) -> None:
        self.__wizard = wizard
        self.__boss = boss
        self.__is_wizard_turn = is_wizard_turn
        self.__effect_timers = (
            effect_timers if effect_timers else SpellEffectTimers(dict())
        )

    @property
    def wizard(self) -> Wizard:
        return self.__wizard

    @property
    def boss(self) -> Boss:
        return self.__boss

    @property
    def characters_state(self) -> CharactersState:
        return CharactersState(wizard=self.wizard, boss=self.boss)

    @property
    def is_wizard_turn(self) -> bool:
        return self.__is_wizard_turn

    @property
    def effect_timers(self) -> SpellEffectTimers:
        return self.__effect_timers

    def is_over(self) -> bool:
        return self.characters_state.some_is_dead()

    def wizard_won(self) -> bool:
        return self.boss.is_dead()

    def add_spell_effect(self, effect: SpellEffect) -> "GameState":
        new_timers = self.__effect_timers.add_spell_effect(effect)

        return GameState(
            wizard=self.wizard,
            boss=self.boss,
            is_wizard_turn=self.is_wizard_turn,
            effect_timers=new_timers,
        )

    def apply_effects(self) -> "GameState":
        characters = self.characters_state
        effects = sorted(
            self.__effect_timers.active_effects(),
            key=lambda e: int(e.is_high_priority),
            reverse=True,
        )
        for effect in effects:
            if characters.some_is_dead():
                break
            characters = effect.apply(characters)
        new_timers = self.__effect_timers.decrement_timers()
        characters = new_timers.wear_off_effects(characters)
        return GameState(
            wizard=characters.wizard,
            boss=characters.boss,
            is_wizard_turn=self.is_wizard_turn,
            effect_timers=new_timers,
        )

    def effect_countdown(self, effect: SpellEffect) -> int:
        return self.__effect_timers.effect_countdown(effect)

    def __hash__(self) -> int:
        return hash(
            (
                self.wizard,
                self.boss,
                self.is_wizard_turn,
                self.effect_timers,
            )
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, GameState)
            and self.wizard == other.wizard
            and self.boss == other.boss
            and self.is_wizard_turn == other.is_wizard_turn
            and self.effect_timers == other.effect_timers
        )
