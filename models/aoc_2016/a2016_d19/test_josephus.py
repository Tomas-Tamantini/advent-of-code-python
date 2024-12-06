import pytest

from .josephus import josephus, modified_josephus


@pytest.mark.parametrize(
    ("num_players", "expected_winning_position"),
    [
        (1, 1),
        (2, 1),
        (3, 3),
        (4, 1),
        (5, 3),
        (6, 5),
        (7, 7),
        (8, 1),
        (9, 3),
        (10, 5),
        (3012210, 1830117),
    ],
)
def test_josephus_returns_winning_position_for_n_players(
    num_players, expected_winning_position
):
    assert josephus(num_players) == expected_winning_position


@pytest.mark.parametrize(
    ("num_players", "expected_winning_position"),
    [
        (1, 1),
        (2, 1),
        (3, 3),
        (4, 1),
        (5, 2),
        (6, 3),
        (7, 5),
        (8, 7),
        (9, 9),
        (10, 1),
        (11, 2),
        (12, 3),
        (13, 4),
        (14, 5),
        (15, 6),
        (16, 7),
        (17, 8),
        (18, 9),
        (19, 11),
        (20, 13),
        (3012210, 1417887),
    ],
)
def test_modified_josephus_where_player_across_the_circle_gets_killed(
    num_players, expected_winning_position
):
    assert modified_josephus(num_players) == expected_winning_position
