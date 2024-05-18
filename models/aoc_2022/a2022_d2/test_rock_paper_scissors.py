import pytest
from .rock_paper_scissors import RockPaperScissorsAction, rock_paper_scissors_score


@pytest.mark.parametrize(
    "my_action, opponent_action, expected_score",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.PAPER, 1),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.SCISSORS, 2),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.ROCK, 3),
    ],
)
def test_score_for_losing_rock_paper_scissors_is_shape_score(
    my_action, opponent_action, expected_score
):
    assert rock_paper_scissors_score(my_action, opponent_action) == expected_score


@pytest.mark.parametrize(
    "my_action, opponent_action, expected_score",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.ROCK, 4),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.PAPER, 5),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.SCISSORS, 6),
    ],
)
def test_score_for_tying_rock_paper_scissors_is_shape_score_plus_three(
    my_action, opponent_action, expected_score
):
    assert rock_paper_scissors_score(my_action, opponent_action) == expected_score


@pytest.mark.parametrize(
    "my_action, opponent_action, expected_score",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.SCISSORS, 7),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.ROCK, 8),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.PAPER, 9),
    ],
)
def test_score_for_winning_rock_paper_scissors_is_shape_score_plus_six(
    my_action, opponent_action, expected_score
):
    assert rock_paper_scissors_score(my_action, opponent_action) == expected_score
