from typing import Iterator
from models.common.io import InputReader
from .rock_paper_scissors import RockPaperScissorsAction


def parse_rock_paper_scissors(
    input_reader: InputReader,
) -> Iterator[tuple[RockPaperScissorsAction, RockPaperScissorsAction]]:
    left_action_map = {
        "A": RockPaperScissorsAction.ROCK,
        "B": RockPaperScissorsAction.PAPER,
        "C": RockPaperScissorsAction.SCISSORS,
    }
    right_action_map = {
        "X": RockPaperScissorsAction.ROCK,
        "Y": RockPaperScissorsAction.PAPER,
        "Z": RockPaperScissorsAction.SCISSORS,
    }
    for line in input_reader.read_stripped_lines():
        left_action, right_action = line.split()
        yield left_action_map[left_action], right_action_map[right_action]
