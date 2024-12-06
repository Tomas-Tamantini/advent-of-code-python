from .game_engine import InfectionGame
from .game_state import InfectionGameState


def optimal_boost_for_immune_system(
    inital_state: InfectionGameState, binary_search_upper_bound: int = 1000
) -> tuple[int, InfectionGameState]:
    boost_lb = 0
    boost_ub = binary_search_upper_bound
    result = None
    while boost_lb < boost_ub:
        boost = (boost_lb + boost_ub) // 2
        game = InfectionGame(inital_state.boost_immune_system_attack_power(boost))
        immune_system_won = False
        try:
            game.run_until_over()
            immune_system_won = game.immune_system_won
        except ValueError:
            pass
        if immune_system_won:
            boost_ub = boost
            if result is None or result[0] > boost:
                result = (boost, game.state)
        else:
            boost_lb = boost + 1
    if result is None:
        return optimal_boost_for_immune_system(
            inital_state, binary_search_upper_bound * 10
        )
    else:
        return result
