from dataclasses import dataclass
from .cave_game import CaveGame
from .bot_moves import CaveGameBot


@dataclass(frozen=True)
class OptimalGameResults:
    rounds: int
    hp_remaining: int
    elf_attack_power: int


def optimal_game_for_elves(
    game: CaveGame, bot: CaveGameBot, binary_search_upper_bound: int = 100
) -> OptimalGameResults:
    cave = game.cave_map
    initial_state = game.state
    attack_power_lb = 0
    attack_power_ub = binary_search_upper_bound
    result = None
    while attack_power_lb < attack_power_ub:
        attack_power = (attack_power_lb + attack_power_ub) // 2
        game = CaveGame(cave, initial_state.set_elf_attack_power(attack_power))
        game.play_until_over(bot)
        if game.elf_casualties == 0:
            attack_power_ub = attack_power
            if result is None or result.elf_attack_power > attack_power:
                result = OptimalGameResults(
                    rounds=game.round,
                    hp_remaining=game.state.total_hp,
                    elf_attack_power=attack_power,
                )
        else:
            attack_power_lb = attack_power + 1

    if result is None:
        raise ValueError(
            f"No optimal game found - Elf attack power must be greater than {binary_search_upper_bound}"
        )
    return result
