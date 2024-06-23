from models.common.io import IOHandler
from .logic import (
    CaveGameBotAttackWeakest,
    build_cave_game,
    CaveTeamSpec,
    optimal_game_for_elves,
)


def aoc_2018_d15(io_handler: IOHandler) -> None:
    print("--- AOC 2018 - Day 15: Beverage Bandits ---")
    map_with_units = io_handler.input_reader.read()
    elf_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    goblin_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    outcome = game.round * game.state.total_hp
    print(f"Part 1: Outcome of combat: {outcome}")
    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    results = optimal_game_for_elves(game, bot=CaveGameBotAttackWeakest())
    outcome = results.rounds * results.hp_remaining
    print(
        f"Part 2: Outcome of combat with optimal elf attack power ({results.elf_attack_power}): {outcome}"
    )
