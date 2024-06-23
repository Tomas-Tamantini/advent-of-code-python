from models.common.io import IOHandler, Problem
from .logic import InfectionGame, optimal_boost_for_immune_system
from .parser import parse_infection_game


def aoc_2018_d24(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 24, "Immune System Simulator 20XX")
    io_handler.output_writer.write_header(problem_id)
    initial_game_state = parse_infection_game(io_handler.input_reader)
    game = InfectionGame(initial_game_state)
    game.run_until_over()
    num_units = game.state.total_num_units
    print(f"Part 1: Number of units remaining: {num_units}")
    _, final_state = optimal_boost_for_immune_system(initial_game_state)
    num_units = final_state.total_num_units
    print(f"Part 2: Number of units remaining with optimal boost: {num_units}")
