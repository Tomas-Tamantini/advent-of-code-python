from models.common.io import InputReader
from .parser import parse_rock_paper_scissors
from .rock_paper_scissors import rock_paper_scissors_score


def aoc_2022_d2(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 2: Rock Paper Scissors ---")
    score = 0
    for opponent_action, my_action in parse_rock_paper_scissors(input_reader):
        score += rock_paper_scissors_score(my_action, opponent_action)
    print(f"Part 1: Total score is {score}")
