import pytest
from .rock_paper_scissors import (
    RockPaperScissorsAction,
    rock_paper_scissors_score,
    RockPaperScissorsResult,
    my_rock_paper_scissors_action_from_result,
)


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


@pytest.mark.parametrize(
    "opponent_action, my_action",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.ROCK),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.PAPER),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.SCISSORS),
    ],
)
def test_to_tie_in_rock_paper_scissors_one_should_play_the_same_action(
    opponent_action, my_action
):
    result = RockPaperScissorsResult.TIE
    assert (
        my_rock_paper_scissors_action_from_result(result, opponent_action) == my_action
    )


@pytest.mark.parametrize(
    "opponent_action, my_action",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.SCISSORS),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.ROCK),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.PAPER),
    ],
)
def test_to_lose_in_rock_paper_scissors_one_should_play_the_losing_action(
    opponent_action, my_action
):
    result = RockPaperScissorsResult.LOSE
    assert (
        my_rock_paper_scissors_action_from_result(result, opponent_action) == my_action
    )


@pytest.mark.parametrize(
    "opponent_action, my_action",
    [
        (RockPaperScissorsAction.ROCK, RockPaperScissorsAction.PAPER),
        (RockPaperScissorsAction.PAPER, RockPaperScissorsAction.SCISSORS),
        (RockPaperScissorsAction.SCISSORS, RockPaperScissorsAction.ROCK),
    ],
)
def test_to_win_in_rock_paper_scissors_one_should_play_the_winning_action(
    opponent_action, my_action
):
    result = RockPaperScissorsResult.WIN
    assert (
        my_rock_paper_scissors_action_from_result(result, opponent_action) == my_action
    )
