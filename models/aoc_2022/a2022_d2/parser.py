from typing import Iterator
from models.common.io import InputReader
from .rock_paper_scissors import (
    RockPaperScissorsAction,
    RockPaperScissorsResult,
    my_rock_paper_scissors_action_from_result,
)

_left_action_map = {
    "A": RockPaperScissorsAction.ROCK,
    "B": RockPaperScissorsAction.PAPER,
    "C": RockPaperScissorsAction.SCISSORS,
}
_right_action_map = {
    "X": RockPaperScissorsAction.ROCK,
    "Y": RockPaperScissorsAction.PAPER,
    "Z": RockPaperScissorsAction.SCISSORS,
}
_result_map = {
    "X": RockPaperScissorsResult.LOSE,
    "Y": RockPaperScissorsResult.TIE,
    "Z": RockPaperScissorsResult.WIN,
}


def parse_rock_paper_scissors(
    input_reader: InputReader, interpret_as_result: bool = False
) -> Iterator[tuple[RockPaperScissorsAction, RockPaperScissorsAction]]:

    for line in input_reader.read_stripped_lines():
        left_action_chr, right_action_chr = line.split()
        left_action = _left_action_map[left_action_chr]
        right_action = (
            my_rock_paper_scissors_action_from_result(
                result=_result_map[right_action_chr], opponent_action=left_action
            )
            if interpret_as_result
            else _right_action_map[right_action_chr]
        )
        yield left_action, right_action
