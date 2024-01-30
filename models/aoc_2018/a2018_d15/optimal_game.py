from dataclasses import dataclass
from .cave_game import CaveGame
from .bot_moves import CaveGameBot


@dataclass(frozen=True)
class OptimalGameResults:
    rounds: int
    hp_remaining: int
    elf_attack_power: int


def optimal_game_for_elves(
    game: CaveGame, bot: CaveGameBot, binary_search_upper_bound: int = 30
) -> OptimalGameResults:
    cave = game.cave_map
    initial_state = game.state
    attack_power_lb = 0
    attack_power_ub = binary_search_upper_bound
    result = None
    while attack_power_lb < attack_power_ub:
        attack_power = (attack_power_lb + attack_power_ub) // 2
        new_game = CaveGame(cave, initial_state.set_elf_attack_power(attack_power))
        new_game.play_until_over(bot)
        if new_game.elf_casualties == 0:
            attack_power_ub = attack_power
            if result is None or result.elf_attack_power > attack_power:
                result = OptimalGameResults(
                    rounds=new_game.round,
                    hp_remaining=new_game.state.total_hp,
                    elf_attack_power=attack_power,
                )
        else:
            attack_power_lb = attack_power + 1

    if result is None:
        new_boundary = binary_search_upper_bound * 10
        return optimal_game_for_elves(game, bot, new_boundary)
    else:
        return result
