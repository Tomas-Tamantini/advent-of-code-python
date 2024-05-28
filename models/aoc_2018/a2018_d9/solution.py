from models.common.io import InputReader, ProgressBarConsole
from .marble_game import marble_game_score


def aoc_2018_d9(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2018 - Day 9: Marble Mania ---")
    line = input_reader.read()
    num_players, last_marble = map(int, [line.split()[0], line.split()[-2]])
    scores = marble_game_score(num_players, last_marble)
    print(f"Part 1: Winning score up to marble {last_marble}: {max(scores.values())}")
    scores = marble_game_score(num_players, last_marble * 100, progress_bar)
    print(
        f"Part 2: Winning score up to marble {last_marble * 100}: {max(scores.values())}"
    )
