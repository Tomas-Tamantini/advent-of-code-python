from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_players_starting_positions
from .logic import (
    DiracDiceStartingConfiguration,
    play_deterministic_dirac_dice,
    QuantumDiracGame,
)


def aoc_2021_d21(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 21, "Dirac Dice")
    io_handler.output_writer.write_header(problem_id)
    starting_spaces = parse_players_starting_positions(io_handler.input_reader)
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=1000, starting_spaces=starting_spaces
    )
    final_state = play_deterministic_dirac_dice(starting_configuration)
    result = final_state.worst_score * final_state.num_dice_rolls
    solution = ProblemSolution(
        problem_id,
        f"The product of the worst score and number of dice rolls is {result}",
        part=1,
    )
    io_handler.set_solution(solution)
    starting_configuration = DiracDiceStartingConfiguration(
        board_size=10, goal_score=21, starting_spaces=starting_spaces
    )
    quantum_game = QuantumDiracGame(starting_configuration)
    num_wins = quantum_game.num_wins(first_player_win=True)
    solution = ProblemSolution(
        problem_id, f"The number of wins for the first player is {num_wins}", part=2
    )
    io_handler.set_solution(solution)
