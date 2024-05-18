import pytest
from models.common.cellular_automata import (
    ElementaryAutomaton,
    OneDimensionalBinaryCelullarAutomaton,
    GameOfLife,
    LangtonsAnt,
    MultiStateLangtonsAnt,
    AntState,
)
from models.common.vectors import Vector2D, CardinalDirection, TurnDirection


def test_unidimensional_automaton_cannot_have_all_zeroes_turn_into_one_rule():
    with pytest.raises(ValueError):
        _ = OneDimensionalBinaryCelullarAutomaton(rules={(0, 0, 0): 1})


def test_all_rules_for_unidimensional_automaton_must_have_same_length():
    with pytest.raises(ValueError):
        _ = OneDimensionalBinaryCelullarAutomaton(rules={(1, 1, 1): 0, (1,): 1})


def test_all_rules_for_unidimensional_automaton_must_have_odd_length():
    with pytest.raises(ValueError):
        _ = OneDimensionalBinaryCelullarAutomaton(rules={(1, 1): 1})


def test_one_dimensional_binary_automaton_follows_given_rules_assuming_zero_for_omitted_rules():
    automaton = OneDimensionalBinaryCelullarAutomaton(
        rules={(0, 0, 1): 1, (1, 0, 1): 1}
    )
    assert automaton.next_state({}) == set()
    assert automaton.next_state({0}) == {-1}
    assert automaton.next_state({1, 3}) == {0, 2}


def test_one_dimensional_binary_automaton_can_have_radius_of_influence_larger_than_one():
    automaton = OneDimensionalBinaryCelullarAutomaton(rules={(0, 0, 0, 0, 1): 1})
    assert automaton.next_state({0}) == {-2}


def test_elementary_automaton_rule_index_must_be_between_0_and_255():
    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=-1)

    with pytest.raises(ValueError):
        _ = ElementaryAutomaton(rule=256)


def test_elementary_automaton_rule_zero_switches_off_all_cells():
    automaton = ElementaryAutomaton(rule=0)
    current_state = {1, 2, 3}
    assert automaton.next_state(current_state) == set()


def test_elementary_automaton_rule_110_produces_A117999_OEIS_sequence():
    automaton = ElementaryAutomaton(rule=110)
    expected_states = [
        {4},
        {3, 4},
        {2, 3, 4},
        {1, 2, 4},
        {0, 1, 2, 3, 4},
    ]
    for i in range(1, len(expected_states)):
        assert automaton.next_state(expected_states[i - 1]) == expected_states[i]


def test_gof_cell_which_is_off_and_has_less_than_3_neighbors_stays_off():
    game = GameOfLife()
    assert Vector2D(1, 1) not in game.next_state(set())
    assert Vector2D(1, 1) not in game.next_state({Vector2D(0, 0)})
    assert Vector2D(1, 1) not in game.next_state({Vector2D(0, 0), Vector2D(0, 1)})


def test_gof_cell_which_is_off_and_has_more_than_3_neighbors_stays_off():
    game = GameOfLife()
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0)}
    )
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0), Vector2D(2, 0)}
    )


def test_gof_cell_which_is_on_and_has_less_than_two_neighbors_dies():
    game = GameOfLife()
    assert Vector2D(1, 1) not in game.next_state({Vector2D(1, 1)})
    assert Vector2D(1, 1) not in game.next_state({Vector2D(1, 1), Vector2D(0, 0)})


def test_gof_cell_which_is_on_and_has_more_than_three_neighbors_dies():
    game = GameOfLife()
    assert Vector2D(1, 1) not in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 0)}
    )
    assert Vector2D(1, 1) not in game.next_state(
        {
            Vector2D(1, 1),
            Vector2D(0, 0),
            Vector2D(0, 1),
            Vector2D(0, 2),
            Vector2D(1, 0),
            Vector2D(2, 0),
        }
    )


def test_gof_cell_which_is_on_and_has_two_or_three_neighbors_survives():
    game = GameOfLife()
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1)}
    )
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(1, 1), Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 2)}
    )


def test_gof_cell_which_is_off_and_has_three_neighbors_comes_alive():
    game = GameOfLife()
    assert Vector2D(1, 1) in game.next_state(
        {Vector2D(0, 0), Vector2D(0, 1), Vector2D(2, 2)}
    )


def test_gof_cell_outside_grid_never_comes_alive():
    game = GameOfLife(width=3, height=3)
    assert (3, 1) not in game.next_state(
        {Vector2D(2, 0), Vector2D(2, 1), Vector2D(2, 2)}
    )


def test_at_an_off_square_ant_flips_square_then_turns_right_and_moves_forward():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_cells=set())
    ant.walk()
    assert ant.position == Vector2D(1, 0)
    assert ant.direction == CardinalDirection.EAST
    assert ant.on_cells == {Vector2D(0, 0)}


def test_at_an_on_square_ant_flips_square_then_turns_left_and_moves_forward():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_cells={Vector2D(0, 0)})
    ant.walk()
    assert ant.position == Vector2D(-1, 0)
    assert ant.direction == CardinalDirection.WEST
    assert ant.on_cells == set()


def test_after_transitional_phase_ant_builds_highway_with_period_104():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    ant = LangtonsAnt(initial_state, initial_on_cells=set())
    positions = []
    directions = []
    num_on_cells = []
    for i in range(13_000):
        ant.walk()
        if i > 11_000 and i % 104 == 0:
            positions.append(ant.position)
            directions.append(ant.direction)
            num_on_cells.append(len(ant.on_cells))
    for i in range(len(positions) - 1):
        assert directions[i + 1] == directions[i]
        assert positions[i + 1].x == positions[i].x - 2
        assert positions[i + 1].y == positions[i].y - 2
        assert num_on_cells[i + 1] == num_on_cells[i] + 12


def test_ant_that_always_turns_right_walks_in_a_circle():
    initial_state = AntState(position=Vector2D(0, 0), direction=CardinalDirection.WEST)
    cells = {
        Vector2D(0, 0): 1,
        Vector2D(10, 0): 1,
        Vector2D(10, 10): 1,
        Vector2D(0, 10): 1,
    }
    default_state = 0
    rule = {
        0: (0, TurnDirection.NO_TURN),
        1: (2, TurnDirection.RIGHT),
        2: (1, TurnDirection.RIGHT),
    }
    ant = MultiStateLangtonsAnt(initial_state, cells, default_state, rule)
    for _ in range(40):
        ant.walk()
    assert ant.position == Vector2D(0, 0)
    assert ant.direction == CardinalDirection.WEST
    assert ant.current_cell == 2
