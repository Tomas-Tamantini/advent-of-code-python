from models.common.io import IOHandler
from .parser import parse_rock_paper_scissors
from .rock_paper_scissors import rock_paper_scissors_score


def aoc_2022_d2(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2022 - Day 2: Rock Paper Scissors ---")
    score = sum(
        rock_paper_scissors_score(my_action, opponent_action)
        for opponent_action, my_action in parse_rock_paper_scissors(
            io_handler.input_reader
        )
    )
    print(f"Part 1: Total score parsing XYZ as actions is {score}")
    score = sum(
        rock_paper_scissors_score(my_action, opponent_action)
        for opponent_action, my_action in parse_rock_paper_scissors(
            io_handler.input_reader, interpret_as_result=True
        )
    )
    print(f"Part 2: Total score parsing XYZ as results is {score}")
