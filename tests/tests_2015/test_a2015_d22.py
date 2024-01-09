import pytest
from unittest import mock
from math import inf
from models.aoc_2015.a2015_d22 import (
    GameState,
    Boss,
    Wizard,
    CharactersState,
    SpellEffect,
    SpellEffectTimers,
    ShieldEffect,
    PoisonEffect,
    RechargeEffect,
    DrainWizardHealthEffect,
    BossMove,
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
    min_mana_to_defeat_boss,
)


def _build_game_state(
    wizard: Wizard = None,
    boss: Boss = None,
    is_wizard_turn: bool = True,
    effect_timers: SpellEffectTimers = None,
) -> GameState:
    if wizard is None:
        wizard = mock.MagicMock(Wizard)
        wizard.is_dead.return_value = False
        wizard.mana = 500
    if boss is None:
        boss = mock.MagicMock(Boss)
        boss.is_dead.return_value = False
    if effect_timers is None:
        effect_timers = SpellEffectTimers(dict())
    return GameState(wizard, boss, is_wizard_turn, effect_timers)


def _build_magic_missile(mana_cost: int = 60, damage: int = 4) -> MagicMissile:
    return MagicMissile(mana_cost=mana_cost, damage=damage)


def _build_drain(mana_cost: int = 73, damage: int = 2, heal: int = 2) -> Drain:
    return Drain(mana_cost=mana_cost, damage=damage, heal=heal)


def _build_shield(mana_cost: int = 113, duration: int = 6, armor: int = 7) -> Shield:
    return Shield(mana_cost=mana_cost, duration=duration, armor=armor)


def _build_poison(mana_cost: int = 173, duration: int = 6, damage: int = 3) -> Poison:
    return Poison(mana_cost=mana_cost, duration=duration, damage=damage)


def _build_recharge(
    mana_cost: int = 229, duration: int = 5, mana_recharge: int = 101
) -> Recharge:
    return Recharge(mana_cost=mana_cost, duration=duration, mana_recharge=mana_recharge)


def _build_boss_move(damage: int = 8) -> BossMove:
    return BossMove(damage=damage)


def _build_wizard(hit_points: int = 10, mana: int = 250, armor: int = 0) -> Wizard:
    return Wizard(hit_points=hit_points, mana=mana, armor=armor)


def test_game_is_over_if_wizard_is_dead():
    dead_wizard = mock.MagicMock(Wizard)
    dead_wizard.is_dead.return_value = True
    game_state = _build_game_state(wizard=dead_wizard)
    assert game_state.is_over() is True


def test_game_is_over_if_boss_is_dead():
    dead_boss = mock.MagicMock(Boss)
    dead_boss.is_dead.return_value = True
    game_state = _build_game_state(boss=dead_boss)
    assert game_state.is_over() is True


def test_game_is_not_over_if_both_characters_are_not_dead():
    alive_character = mock.MagicMock()
    alive_character.is_dead.return_value = False
    game_state = _build_game_state(boss=alive_character, wizard=alive_character)
    assert game_state.is_over() is False


def test_wizard_won_if_boss_is_dead():
    dead_boss = mock.MagicMock(Boss)
    dead_boss.is_dead.return_value = True
    game_state = _build_game_state(boss=dead_boss)
    assert game_state.wizard_won() is True


def test_wizard_did_not_win_if_boss_is_not_dead():
    alive_character = mock.MagicMock()
    alive_character.is_dead.return_value = False
    game_state = _build_game_state(boss=alive_character, wizard=alive_character)
    assert game_state.wizard_won() is False


@pytest.mark.parametrize(
    "move",
    [
        _build_boss_move(),
        _build_magic_missile(),
        _build_drain(),
        _build_shield(),
        _build_poison(),
        _build_recharge(),
    ],
)
def test_game_move_alternates_turn(move):
    game_state = _build_game_state(is_wizard_turn=True)
    new_state = move.apply(game_state)
    assert new_state.is_wizard_turn is False


@pytest.mark.parametrize(
    "spell",
    [
        _build_magic_missile(mana_cost=60),
        _build_drain(mana_cost=73),
        _build_shield(mana_cost=113),
        _build_poison(mana_cost=173),
        _build_recharge(mana_cost=229),
    ],
)
def test_spell_cannot_be_cast_if_not_enough_mana(spell):
    wizard = mock.MagicMock(Wizard)
    wizard.mana = 59
    game_state = _build_game_state(wizard=wizard)
    with pytest.raises(ValueError):
        spell.apply(game_state)


@pytest.mark.parametrize(
    "spell",
    [
        _build_magic_missile(mana_cost=60),
        _build_shield(mana_cost=113),
        _build_poison(mana_cost=173),
        _build_recharge(mana_cost=229),
    ],
)
def test_spells_spend_mana(spell):
    wizard = mock.MagicMock(Wizard)
    wizard.mana = 500
    poorer_wizard = mock.MagicMock(Wizard)
    wizard.spend_mana.return_value = poorer_wizard
    game_state = _build_game_state(wizard=wizard)
    new_state = spell.apply(game_state)
    wizard.spend_mana.assert_called_once_with(spell._mana_cost)
    assert new_state.wizard == poorer_wizard


def test_magic_missile_deals_damage():
    boss = mock.MagicMock(Boss)
    damaged_boss = mock.MagicMock(Boss)
    boss.take_damage.return_value = damaged_boss
    game_state = _build_game_state(boss=boss)
    new_state = _build_magic_missile(damage=4).apply(game_state)
    boss.take_damage.assert_called_once_with(4)
    assert new_state.boss == damaged_boss


def test_drain_spends_mana_to_heal_wizard():
    wizard = mock.MagicMock(Wizard)
    poorer_wizard = mock.MagicMock(Wizard)
    healed_wizard = mock.MagicMock(Wizard)
    wizard.mana = 500
    wizard.spend_mana.return_value = poorer_wizard
    poorer_wizard.heal.return_value = healed_wizard
    game_state = _build_game_state(wizard=wizard)
    new_state = _build_drain(mana_cost=73, heal=2).apply(game_state)
    wizard.spend_mana.assert_called_once_with(73)
    poorer_wizard.heal.assert_called_once_with(2)
    assert new_state.wizard == healed_wizard


def test_drain_deals_damage():
    boss = mock.MagicMock(Boss)
    damaged_boss = mock.MagicMock(Boss)
    boss.take_damage.return_value = damaged_boss
    game_state = _build_game_state(boss=boss)
    new_state = _build_drain(damage=2).apply(game_state)
    boss.take_damage.assert_called_once_with(2)
    assert new_state.boss == damaged_boss


def test_can_add_effect_to_game_state():
    game_state = _build_game_state()
    effect = SpellEffect(id="test", duration=2)
    new_state = game_state.add_spell_effect(effect)
    assert new_state.effect_countdown(effect) == 2


def test_cannot_add_two_effects_with_same_id():
    game_state = _build_game_state()
    effect_a = SpellEffect(id="duplicate_id", duration=2)
    effect_b = SpellEffect(id="duplicate_id", duration=3)
    new_state = game_state.add_spell_effect(effect_a)
    with pytest.raises(ValueError):
        new_state.add_spell_effect(effect_b)


def test_can_apply_effects_and_modify_characters_state():
    wizard_original = _build_wizard(hit_points=10)
    boss_original = Boss(hit_points=10)
    characters_original = CharactersState(wizard_original, boss_original)
    characters_after_a = CharactersState(
        _build_wizard(hit_points=9), Boss(hit_points=10)
    )
    characters_after_b = CharactersState(
        _build_wizard(hit_points=9), Boss(hit_points=10)
    )
    effect_a = mock.MagicMock(SpellEffect)
    effect_a.apply.return_value = characters_after_a
    effect_a.duration = 2
    effect_b = mock.MagicMock(SpellEffect)
    effect_b.apply.return_value = characters_after_b
    effect_b.duration = 3
    game_state = _build_game_state(
        wizard_original,
        boss_original,
        effect_timers=SpellEffectTimers({effect_a: 2, effect_b: 3}),
    )
    new_state = game_state.apply_effects()
    if new_state.characters_state == characters_after_b:
        effect_a.apply.assert_called_once_with(characters_original)
        effect_b.apply.assert_called_once_with(characters_after_a)
        assert new_state.characters_state == characters_after_b
    else:
        effect_b.apply.assert_called_once_with(characters_original)
        effect_a.apply.assert_called_once_with(characters_after_b)
        assert new_state.characters_state == characters_after_a


def test_applying_an_effect_decrements_its_counter():
    effect = mock.MagicMock(SpellEffect)
    game_state = _build_game_state(effect_timers=SpellEffectTimers({effect: 2}))
    new_state = game_state.apply_effects()
    assert game_state.effect_countdown(effect) == 2
    assert new_state.effect_countdown(effect) == 1


def test_effect_wears_off_when_countdown_reaches_zero():
    characters_without_effect = CharactersState(
        mock.MagicMock(Wizard), mock.MagicMock(Boss)
    )
    effect = mock.MagicMock(SpellEffect)
    effect.wear_off.return_value = characters_without_effect
    game_state = _build_game_state(effect_timers=SpellEffectTimers({effect: 1}))
    new_state = game_state.apply_effects()
    assert new_state.effect_countdown(effect) == 0
    effect.wear_off.assert_called_once()
    assert new_state.characters_state == characters_without_effect


@pytest.mark.parametrize("spell_fn", [_build_shield, _build_poison, _build_recharge])
def test_some_spells_add_effects(spell_fn):
    game_state = _build_game_state()
    spell = spell_fn(duration=6)
    new_state = spell.apply(game_state)
    assert new_state.effect_countdown(spell._effect) == 6


def test_shield_adds_armor():
    wizard = mock.MagicMock(Wizard)
    wizard.mana = 500
    wizard.is_dead.return_value = False
    wizard_with_armor = mock.MagicMock(Wizard)
    wizard.add_armor.return_value = wizard_with_armor
    effect = ShieldEffect(id="shield", duration=6, armor=7)
    game_state = _build_game_state(
        wizard=wizard, effect_timers=SpellEffectTimers({effect: 6})
    )
    new_state = game_state.apply_effects()
    wizard.add_armor.assert_called_once_with(7)
    assert new_state.wizard == wizard_with_armor


def test_shield_removes_armor_on_wear_off():
    wizard = mock.MagicMock(Wizard)
    wizard.mana = 500
    wizard_without_armor = mock.MagicMock(Wizard)
    wizard.remove_armor.return_value = wizard_without_armor
    effect = ShieldEffect(id="shield", duration=6, armor=7)
    game_state = _build_game_state(
        wizard=wizard, effect_timers=SpellEffectTimers({effect: 0})
    )
    new_state = game_state.apply_effects()
    wizard.remove_armor.assert_called_once()
    assert new_state.wizard == wizard_without_armor


def test_poison_deals_damage_to_boss():
    boss = mock.MagicMock(Boss)
    boss.is_dead.return_value = False
    damaged_boss = mock.MagicMock(Boss)
    boss.take_damage.return_value = damaged_boss
    effect = PoisonEffect(id="poison", duration=6, damage=3)
    game_state = _build_game_state(
        boss=boss, effect_timers=SpellEffectTimers({effect: 6})
    )
    new_state = game_state.apply_effects()
    boss.take_damage.assert_called_once_with(3)
    assert new_state.boss == damaged_boss


def test_recharge_adds_mana_to_wizard():
    wizard = mock.MagicMock(Wizard)
    wizard.mana = 500
    wizard.is_dead.return_value = False
    wizard_with_mana = mock.MagicMock(Wizard)
    wizard.recharge_mana.return_value = wizard_with_mana
    effect = RechargeEffect(id="recharge", duration=5, mana=101)
    game_state = _build_game_state(
        wizard=wizard, effect_timers=SpellEffectTimers({effect: 5})
    )
    new_state = game_state.apply_effects()
    wizard.recharge_mana.assert_called_once_with(101)
    assert new_state.wizard == wizard_with_mana


def test_drain_wizard_health_deals_damage_to_wizard():
    wizard = mock.MagicMock(Wizard)
    wizard.is_dead.return_value = False
    damaged_wizard = mock.MagicMock(Wizard)
    wizard.take_damage.return_value = damaged_wizard
    effect = DrainWizardHealthEffect(id="drain", duration=5, damage=2)
    game_state = _build_game_state(
        wizard=wizard, effect_timers=SpellEffectTimers({effect: 5})
    )
    new_state = game_state.apply_effects()
    wizard.take_damage.assert_called_once_with(2, ignore_armor=True)
    assert new_state.wizard == damaged_wizard


def test_effects_can_have_priorities():
    characters_after_low = CharactersState(_build_wizard(10), Boss(10))
    characters_after_high = CharactersState(_build_wizard(9), Boss(9))

    effect_low_priority = mock.MagicMock(SpellEffect)
    effect_low_priority.is_high_priority = False
    effect_low_priority.apply.return_value = characters_after_low
    effect_high_priority = mock.MagicMock(SpellEffect)
    effect_high_priority.is_high_priority = True
    effect_high_priority.apply.return_value = characters_after_high

    game_state = _build_game_state(
        effect_timers=SpellEffectTimers(
            {
                effect_low_priority: 6,
                effect_high_priority: 2,
            }
        ),
    )
    new_state = game_state.apply_effects()
    assert new_state.characters_state == characters_after_low


def test_if_some_effect_kills_a_player_other_effects_do_not_run():
    dead_wizard = mock.MagicMock(Wizard)
    dead_wizard.is_dead.return_value = True
    alive_wizard = mock.MagicMock(Wizard)
    alive_wizard.is_dead.return_value = False
    dead_boss = mock.MagicMock(Boss)
    dead_boss.is_dead.return_value = True
    alive_boss = mock.MagicMock(Boss)
    alive_boss.is_dead.return_value = False

    effect_a = mock.MagicMock(SpellEffect)
    effect_a.is_high_priority = True
    effect_a.apply.return_value = CharactersState(dead_wizard, alive_boss)
    effect_b = mock.MagicMock(SpellEffect)
    effect_b.is_high_priority = False
    effect_b.apply.return_value = CharactersState(alive_wizard, dead_boss)
    game_state = _build_game_state(
        wizard=alive_wizard,
        boss=alive_boss,
        effect_timers=SpellEffectTimers({effect_a: 2, effect_b: 2}),
    )
    new_state = game_state.apply_effects()
    effect_a.apply.assert_called_once()
    effect_b.apply.assert_not_called()
    assert new_state.wizard.is_dead()
    assert not new_state.boss.is_dead()


def test_boss_move_deals_damage_to_wizard():
    wizard = mock.MagicMock(Wizard)
    damaged_wizard = mock.MagicMock(Wizard)
    wizard.take_damage.return_value = damaged_wizard
    game_state = _build_game_state(wizard=wizard)
    new_state = _build_boss_move(damage=8).apply(game_state)
    wizard.take_damage.assert_called_once_with(8)
    assert new_state.wizard == damaged_wizard


def test_boss_is_dead_when_hit_points_reach_zero():
    alive_boss = Boss(hit_points=10)
    assert alive_boss.is_dead() is False
    dead_boss = Boss(hit_points=0)
    assert dead_boss.is_dead() is True


def test_damage_decrements_boss_hit_points():
    boss = Boss(hit_points=10)
    damaged_boss = boss.take_damage(4)
    assert damaged_boss.hit_points == 6


def test_wizard_is_dead_when_hit_points_reach_zero():
    alive_wizard = _build_wizard(hit_points=10)
    assert alive_wizard.is_dead() is False
    dead_wizard = _build_wizard(hit_points=0)
    assert dead_wizard.is_dead() is True


def test_wizard_can_heal():
    wizard = _build_wizard(hit_points=10)
    healed_wizard = wizard.heal(2)
    assert healed_wizard.hit_points == 12


def test_wizard_can_spend_mana():
    wizard = _build_wizard(mana=10)
    poorer_wizard = wizard.spend_mana(2)
    assert poorer_wizard.mana == 8


def test_wizard_can_recharge_mana():
    wizard = _build_wizard(mana=10)
    richer_wizard = wizard.recharge_mana(2)
    assert richer_wizard.mana == 12


def test_wizard_can_add_armor():
    wizard = _build_wizard(armor=10)
    armored_wizard = wizard.add_armor(2)
    assert armored_wizard.armor == 2


def test_wizard_can_remove_armor():
    wizard = _build_wizard(armor=10)
    unarmored_wizard = wizard.remove_armor()
    assert unarmored_wizard.armor == 0


def test_damage_is_deducted_from_wizard_hit_points():
    wizard = _build_wizard(hit_points=10, armor=0)
    damaged_wizard = wizard.take_damage(4)
    assert damaged_wizard.hit_points == 6


def test_armor_reduces_damage():
    wizard = _build_wizard(hit_points=10, armor=2)
    damaged_wizard = wizard.take_damage(4)
    assert damaged_wizard.hit_points == 8


def test_damage_cannot_be_reduced_to_less_than_one():
    wizard = _build_wizard(hit_points=10, armor=20)
    damaged_wizard = wizard.take_damage(4)
    assert damaged_wizard.hit_points == 9


def test_armor_can_be_ignored():
    wizard = _build_wizard(hit_points=10, armor=2)
    damaged_wizard = wizard.take_damage(4, ignore_armor=True)
    assert damaged_wizard.hit_points == 6


def test_if_no_spells_available_min_mana_to_defeat_boss_is_infinite():
    game_state = _build_game_state()
    spell_book = []
    boss_move = _build_boss_move()
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == inf


def test_if_no_winning_strategy_min_mana_to_defeat_boss_is_infinite():
    wizard = Wizard(hit_points=10, mana=250, armor=0)
    boss = Boss(hit_points=13)
    boss_move = BossMove(damage=10)
    game_state = GameState(wizard, boss, is_wizard_turn=False)
    spell_book = [MagicMissile(mana_cost=53, damage=4)]
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == inf


def test_if_wizard_already_won_min_mana_to_defeat_boss_is_zero():
    wizard = Wizard(hit_points=10, mana=250, armor=0)
    boss = Boss(hit_points=0)
    boss_move = BossMove(damage=8)
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [MagicMissile(mana_cost=53, damage=4)]
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == 0


def test_if_multiple_ways_to_defeat_boss_cheapest_one_is_chosen():
    wizard = Wizard(hit_points=10, mana=250, armor=0)
    boss = Boss(hit_points=5)
    boss_move = BossMove(damage=8)
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [
        MagicMissile(mana_cost=53, damage=4),
        Drain(mana_cost=50, damage=2, heal=2),
    ]
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == 103


def test_game_can_last_multiple_rounds():
    wizard = Wizard(hit_points=10, mana=250, armor=0)
    boss = Boss(hit_points=13)
    boss_move = BossMove(damage=8)
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [
        MagicMissile(mana_cost=53, damage=4),
        Drain(mana_cost=73, damage=2, heal=2),
        Shield(mana_cost=113, duration=6, armor=7),
        Poison(mana_cost=173, duration=6, damage=3),
        Recharge(mana_cost=229, duration=5, mana_recharge=101),
    ]
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == 226

    stronger_boss = Boss(hit_points=14)
    game_state = GameState(wizard, stronger_boss, is_wizard_turn=True)
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == 641


def test_game_state_is_hashable():
    game_state_a = GameState(
        wizard=Wizard(hit_points=10, mana=250, armor=0),
        boss=Boss(hit_points=13),
        is_wizard_turn=False,
        effect_timers=SpellEffectTimers(dict()),
    )
    game_state_a = game_state_a.add_spell_effect(
        ShieldEffect(id="shield", duration=6, armor=7)
    )

    game_state_b = GameState(
        wizard=Wizard(hit_points=10, mana=250, armor=0),
        boss=Boss(hit_points=13),
        is_wizard_turn=False,
        effect_timers=SpellEffectTimers({SpellEffect(id="shield", duration=10): 6}),
    )

    assert hash(game_state_a) == hash(game_state_b)
    assert game_state_a == game_state_b


def test_optimizing_winning_strategy_runs_efficiently():
    wizard = Wizard(hit_points=20, mana=500)
    boss = Boss(hit_points=28)
    boss_move = BossMove(damage=9)
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [
        MagicMissile(mana_cost=53, damage=4),
        Drain(mana_cost=73, damage=2, heal=2),
        Shield(mana_cost=113, duration=6, armor=7),
        Poison(mana_cost=173, duration=6, damage=3),
        Recharge(mana_cost=229, duration=5, mana_recharge=101),
    ]
    assert min_mana_to_defeat_boss(game_state, spell_book, boss_move) == 445
