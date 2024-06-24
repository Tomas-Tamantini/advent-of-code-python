from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import (
    CaveGameBotAttackWeakest,
    build_cave_game,
    CaveTeamSpec,
    optimal_game_for_elves,
)


def aoc_2018_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 15, "Beverage Bandits")
    io_handler.output_writer.write_header(problem_id)
    map_with_units = io_handler.input_reader.read()
    elf_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    goblin_specs = CaveTeamSpec(attack_power=3, hit_points=200)
    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    result = game.round * game.state.total_hp
    yield ProblemSolution(problem_id, f"Outcome of combat: {result}", result, part=1)

    game = build_cave_game(map_with_units, elf_specs, goblin_specs)
    results = optimal_game_for_elves(game, bot=CaveGameBotAttackWeakest())
    result = results.rounds * results.hp_remaining
    yield ProblemSolution(
        problem_id,
        f"Outcome of combat with optimal elf attack power ({results.elf_attack_power}): {result}",
        result,
        part=2,
    )
