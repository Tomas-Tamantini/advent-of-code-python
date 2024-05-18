from models.common.io import InputFromString
from .rock_paper_scissors import RockPaperScissorsAction
from .parser import parse_rock_paper_scissors


def test_parse_rock_paper_scissors():
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
