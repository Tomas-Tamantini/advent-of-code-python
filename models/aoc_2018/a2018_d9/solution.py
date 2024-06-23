from models.common.io import IOHandler, Problem
from .marble_game import marble_game_score


def aoc_2018_d9(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 9, "Marble Mania")
    io_handler.output_writer.write_header(problem_id)
    line = io_handler.input_reader.read()
    num_players, last_marble = map(int, [line.split()[0], line.split()[-2]])
    scores = marble_game_score(num_players, last_marble)
    print(f"Part 1: Winning score up to marble {last_marble}: {max(scores.values())}")
    scores = marble_game_score(num_players, last_marble * 100, io_handler.progress_bar)
    print(
        f"Part 2: Winning score up to marble {last_marble * 100}: {max(scores.values())}"
    )
