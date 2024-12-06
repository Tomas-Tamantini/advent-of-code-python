from models.common.io import InputFromString

from ..parser import parse_rock_paper_scissors
from ..rock_paper_scissors import RockPaperScissorsAction


def test_parse_rock_paper_scissors_with_actions():
    input_reader = InputFromString(
        """A Y
           B X
           C Z"""
    )
    rounds = list(parse_rock_paper_scissors(input_reader))
    assert rounds == [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.PAPER),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.ROCK),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.SCISSORS),
    ]


def test_parse_rock_paper_scissors_with_results():
    input_reader = InputFromString(
        """A Y
           B X
           C Z"""
    )
    rounds = list(parse_rock_paper_scissors(input_reader, interpret_as_result=True))
    assert rounds == [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.ROCK),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.ROCK),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.ROCK),
    ]
