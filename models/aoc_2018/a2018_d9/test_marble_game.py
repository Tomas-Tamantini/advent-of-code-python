import pytest

from .marble_game import marble_game_score


def test_marble_game_scores_are_zero_before_first_scoring_marble():
    scores = marble_game_score(num_players=2, last_marble=22)
    assert scores == {1: 0, 2: 0}


def test_scoring_marbles_are_multiples_of_23():
    scores = marble_game_score(num_players=9, last_marble=25)
    assert scores == {i: (32 if i == 5 else 0) for i in range(1, 10)}


@pytest.mark.parametrize(
    ("num_players", "last_marble", "expected_score"),
    [
        (10, 1618, 8317),
        (13, 7999, 146373),
    ],
)
def test_marble_game_runs_efficiently(num_players, last_marble, expected_score):
    scores = marble_game_score(num_players, last_marble)
    assert max(scores.values()) == expected_score
