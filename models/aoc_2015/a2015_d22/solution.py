from models.common.io import IOHandler
from .logic import (
    Wizard,
    Boss,
    BossMove,
    GameState,
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
    DrainWizardHealthEffect,
    min_mana_to_defeat_boss,
)
from models.aoc_2015.a2015_d21.parser import parse_rpg_boss


def aoc_2015_d22(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2015 - Day 22: Wizard Simulator 20XX ---")
    wizard = Wizard(hit_points=50, mana=500)
    boss_kwargs = parse_rpg_boss(io_handler.input_reader)
    boss = Boss(hit_points=boss_kwargs["hit_points"])
    boss_move = BossMove(damage=boss_kwargs["damage"])
    game_state = GameState(wizard, boss, is_wizard_turn=True)
    spell_book = [
        MagicMissile(mana_cost=53, damage=4),
        Drain(mana_cost=73, damage=2, heal=2),
        Shield(mana_cost=113, duration=6, armor=7),
        Poison(mana_cost=173, duration=6, damage=3),
        Recharge(mana_cost=229, duration=5, mana_recharge=101),
    ]
    min_mana = min_mana_to_defeat_boss(game_state, spell_book, boss_move)
    print(f"Part 1: Minimum mana to defeat boss is {min_mana}")

    drain_health = DrainWizardHealthEffect(
        id="drain_health",
        duration=1_000_000,
        damage=1,
        is_high_priority=True,
    )

    game_state_hard_mode = game_state.add_spell_effect(drain_health)
    min_mana = min_mana_to_defeat_boss(game_state_hard_mode, spell_book, boss_move)
    print(f"Part 2: Minimum mana to defeat boss in hard mode is {min_mana}")
