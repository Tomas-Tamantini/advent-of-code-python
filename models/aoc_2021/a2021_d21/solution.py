from models.common.io import IOHandler
from .parser import parse_players_starting_positions
from .logic import (
    DiracDiceStartingConfiguration,
    play_deterministic_dirac_dice,
    QuantumDiracGame,
)


def aoc_2021_d21(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2021 - Day 21: Dirac Dice ---")
    starting_spaces = parse_players_starting_positions(io_handler.input_reader)
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1000, starting_spaces=starting_spaces
    )
    final_state = play_deterministic_dirac_dice(starting_configuration)
    result = final_state.worst_score * final_state.num_dice_rolls
    print(
        f"Part 1: The product of the worst score and number of dice rolls is {result}"
    )
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=21, starting_spaces=starting_spaces
    )
    quantum_game = QuantumDiracGame(starting_configuration)
    num_wins = quantum_game.num_wins(first_player_win=True)
    print(f"Part 2: The number of wins for the first player is {num_wins}")
