import pytest
from models.cellular_automata import ElementaryAutomaton, GameOfLife


def test_rule_index_must_be_between_0_and_255():
    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=-1)

    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=256)


def test_rule_zero_switches_off_all_cells():
    automaton = ElementaryAutomaton(rule=0)
    current_state = "11111"
    assert automaton.next_state(current_state) == "00000"


def test_rule_110_produces_A117999_OEIS_sequence():
    automaton = ElementaryAutomaton(rule=110)
    expected_states = [
        "000010000",
        "000110000",
        "001110000",
        "011010000",
        "111110000",
    ]
    for i in range(1, len(expected_states)):
        assert automaton.next_state(expected_states[i - 1]) == expected_states[i]


def test_gof_cell_which_is_off_and_has_less_than_3_neighbors_stays_off():
    game = GameOfLife()
    assert (1, 1) not in game.next_state(set())
    assert (1, 1) not in game.next_state({(0, 0)})
    assert (1, 1) not in game.next_state({(0, 0), (0, 1)})


def test_gof_cell_which_is_off_and_has_more_than_3_neighbors_stays_off():
    game = GameOfLife()
    assert (1, 1) not in game.next_state({(0, 0), (0, 1), (0, 2), (1, 0)})
    assert (1, 1) not in game.next_state({(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)})


def test_gof_cell_which_is_on_and_has_less_than_two_neighbors_dies():
    game = GameOfLife()
    assert (1, 1) not in game.next_state({(1, 1)})
    assert (1, 1) not in game.next_state({(1, 1), (0, 0)})


def test_gof_cell_which_is_on_and_has_more_than_three_neighbors_dies():
    game = GameOfLife()
    assert (1, 1) not in game.next_state({(1, 1), (0, 0), (0, 1), (0, 2), (1, 0)})
    assert (1, 1) not in game.next_state(
        {(1, 1), (0, 0), (0, 1), (0, 2), (1, 0), (2, 0)}
    )


def test_gof_cell_which_is_on_and_has_two_or_three_neighbors_survives():
    game = GameOfLife()
    assert (1, 1) in game.next_state({(1, 1), (0, 0), (0, 1)})
    assert (1, 1) in game.next_state({(1, 1), (0, 0), (0, 1), (0, 2)})


def test_gof_cell_which_is_off_and_has_three_neighbors_comes_alive():
    game = GameOfLife()
    assert (1, 1) in game.next_state({(0, 0), (0, 1), (2, 2)})


def test_gof_cell_outside_grid_never_comes_alive():
    game = GameOfLife(width=3, height=3)
    assert (3, 1) not in game.next_state({(2, 0), (2, 1), (2, 2)})
