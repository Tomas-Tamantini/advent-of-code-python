import pytest
from models.aoc_2018 import CircularLinkedList, marble_game_score


def test_circular_list_starts_empty():
    cll = CircularLinkedList()
    assert len(cll) == 0


def test_getting_element_from_empty_list_raises_error():
    cll = CircularLinkedList()
    with pytest.raises(IndexError):
        cll.value_at_head


def test_can_add_element_at_head():
    cll = CircularLinkedList()
    cll.add_at_head(123)
    assert len(cll) == 1
    assert cll.value_at_head == 123


def test_can_rotate_list_clockwise():
    cll = CircularLinkedList()
    cll.add_at_head(1)
    cll.add_at_head(2)
    cll.add_at_head(3)
    assert len(cll) == 3
    assert cll.value_at_head == 3
    cll.rotate(steps=1)
    assert cll.value_at_head == 2
    cll.rotate(steps=1)
    assert cll.value_at_head == 1
    cll.rotate(steps=1)
    assert cll.value_at_head == 3
    cll.rotate(steps=2)
    assert cll.value_at_head == 1


def test_can_rotate_list_counterclockwise():
    cll = CircularLinkedList()
    cll.add_at_head(1)
    cll.add_at_head(2)
    cll.add_at_head(3)
    cll.rotate(steps=-1)
    assert cll.value_at_head == 1
    cll.rotate(steps=-1)
    assert cll.value_at_head == 2
    cll.rotate(steps=-1)
    assert cll.value_at_head == 3
    cll.rotate(steps=-2)
    assert cll.value_at_head == 2


def test_can_pop_value_at_head():
    cll = CircularLinkedList()
    cll.add_at_head(1)
    cll.add_at_head(2)
    cll.add_at_head(3)
    cll.add_at_head(4)
    cll.rotate(steps=2)
    value = cll.pop_at_head()
    assert value == 2
    assert len(cll) == 3
    assert cll.value_at_head == 1
    cll.rotate(steps=1)
    assert cll.value_at_head == 4
    cll.rotate(steps=1)
    assert cll.value_at_head == 3
    cll.rotate(steps=1)
    assert cll.value_at_head == 1


def test_cannot_pop_from_empty_list():
    cll = CircularLinkedList()
    with pytest.raises(IndexError):
        cll.pop_at_head()


def test_marble_game_scores_are_zero_before_first_scoring_marble():
    scores = marble_game_score(num_players=2, last_marble=22)
    assert scores == {1: 0, 2: 0}


def test_scoring_marbles_are_multiples_of_23():
    scores = marble_game_score(num_players=9, last_marble=25)
    assert scores == {i: (32 if i == 5 else 0) for i in range(1, 10)}


@pytest.mark.parametrize(
    "num_players, last_marble, expected_score",
    [
        (10, 1618, 8317),
        (13, 7999, 146373),
    ],
)
def test_marble_game_runs_efficiently(num_players, last_marble, expected_score):
    scores = marble_game_score(num_players, last_marble)
    assert max(scores.values()) == expected_score
