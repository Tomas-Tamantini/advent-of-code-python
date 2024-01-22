import pytest
from models.cellular_automata import (
    ElementaryAutomaton,
    GameOfLife,
    LangtonsAnt,
    AntState,
)
from models.vectors import Vector2D, CardinalDirection


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


def test_at_an_off_square_ant_flips_square_then_turns_right_and_moves_forward():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_squares=set())
    ant.walk()
    assert ant.position == Vector2D(1, 0)
    assert ant.direction == CardinalDirection.EAST
    assert ant.on_squares == {Vector2D(0, 0)}


def test_at_an_on_square_ant_flips_square_then_turns_left_and_moves_forward():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_squares={Vector2D(0, 0)})
    ant.walk()
    assert ant.position == Vector2D(-1, 0)
    assert ant.direction == CardinalDirection.WEST
    assert ant.on_squares == set()


def test_after_transitional_phase_ant_builds_highway_with_period_104():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_squares=set())
    positions = []
    directions = []
    num_on_cells = []
    for i in range(13_000):
        ant.walk()
        if i > 11_000 and i % 104 == 0:
            positions.append(ant.position)
            directions.append(ant.direction)
            num_on_cells.append(len(ant.on_squares))
    for i in range(len(positions) - 1):
        assert directions[i + 1] == directions[i]
        assert positions[i + 1].x == positions[i].x - 2
        assert positions[i + 1].y == positions[i].y - 2
        assert num_on_cells[i + 1] == num_on_cells[i] + 12
