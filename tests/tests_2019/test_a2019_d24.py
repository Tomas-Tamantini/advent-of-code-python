import pytest
from models.common.vectors import Vector2D
from models.aoc_2019.a2019_d24 import (
    BugsAutomaton,
    RecursiveBugsAutomaton,
    RecursiveTile,
)


def test_bug_with_no_neighbor_dies():
    automaton = BugsAutomaton(width=3, height=3)
    bug = Vector2D(1, 1)
    next_cells = automaton.next_state({bug})
    assert bug not in next_cells


@pytest.mark.parametrize("num_neighbors", [2, 3, 4])
def test_bug_with_two_or_more_neighbors_dies(num_neighbors):
    automaton = BugsAutomaton(width=3, height=3)
    bug = Vector2D(1, 1)
    live_cells = {bug}
    neighbors = bug.adjacent_positions(include_diagonals=False)
    for _ in range(num_neighbors):
        live_cells.add(next(neighbors))
    next_cells = automaton.next_state(live_cells)
    assert bug not in next_cells


def test_bug_with_one_neighbor_survives():
    automaton = BugsAutomaton(width=3, height=3)
    bug = Vector2D(1, 1)
    neighbor = Vector2D(2, 1)
    next_cells = automaton.next_state({bug, neighbor})
    assert bug in next_cells


def test_empty_space_remains_empty_if_no_neighboring_bugs():
    automaton = BugsAutomaton(width=3, height=3)
    center = Vector2D(1, 1)
    next_cells = automaton.next_state({})
    assert center not in next_cells


@pytest.mark.parametrize("num_neighbors", [3, 4])
def test_empty_space_remains_empty_if_three_or_more_bugs_adjacent(num_neighbors):
    automaton = BugsAutomaton(width=3, height=3)
    center = Vector2D(1, 1)
    live_cells = set()
    neighbors = center.adjacent_positions(include_diagonals=False)
    for _ in range(num_neighbors):
        live_cells.add(next(neighbors))
    next_cells = automaton.next_state(live_cells)
    assert center not in next_cells


@pytest.mark.parametrize("num_neighbors", [1, 2])
def test_empty_space_becomes_infested_if_one_or_two_bugs_adjacent(num_neighbors):
    automaton = BugsAutomaton(width=3, height=3)
    center = Vector2D(1, 1)
    live_cells = set()
    neighbors = center.adjacent_positions(include_diagonals=False)
    for _ in range(num_neighbors):
        live_cells.add(next(neighbors))
    next_cells = automaton.next_state(live_cells)
    assert center in next_cells


def test_biodiversity_rating_for_bugs_automaton_is_sum_of_powers_of_two_for_live_cells():
    live_cells = {Vector2D(0, 3), Vector2D(1, 4)}
    automaton = BugsAutomaton(width=5, height=5)
    assert automaton.biodiversity_rating(live_cells) == 2129920


def test_bugs_automaton_keeps_track_of_previous_patterns_to_find_duplicates():
    initial_configuration = {
        Vector2D(4, 0),
        Vector2D(0, 1),
        Vector2D(3, 1),
        Vector2D(0, 2),
        Vector2D(3, 2),
        Vector2D(4, 2),
        Vector2D(2, 3),
        Vector2D(0, 4),
    }
    automaton = BugsAutomaton(width=5, height=5)
    assert automaton.first_pattern_to_appear_twice(initial_configuration) == {
        Vector2D(0, 3),
        Vector2D(1, 4),
    }


def test_recursive_bugs_automaton_tile_has_four_neighbors_if_not_on_edge():
    tile = RecursiveTile(position=Vector2D(1, 1), level=13)
    automaton = RecursiveBugsAutomaton(width=5, height=5)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 4
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(0, 1), level=13),
        RecursiveTile(position=Vector2D(2, 1), level=13),
        RecursiveTile(position=Vector2D(1, 0), level=13),
        RecursiveTile(position=Vector2D(1, 2), level=13),
    }


def test_recursive_bugs_automaton_tile_has_neighbor_from_level_above_if_on_outer_edge():
    automaton = RecursiveBugsAutomaton(width=5, height=5)

    tile = RecursiveTile(position=Vector2D(0, 0), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 4
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(0, 1), level=13),
        RecursiveTile(position=Vector2D(1, 0), level=13),
        RecursiveTile(position=Vector2D(2, 1), level=14),
        RecursiveTile(position=Vector2D(1, 2), level=14),
    }

    tile = RecursiveTile(position=Vector2D(4, 4), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 4
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(4, 3), level=13),
        RecursiveTile(position=Vector2D(3, 4), level=13),
        RecursiveTile(position=Vector2D(2, 3), level=14),
        RecursiveTile(position=Vector2D(3, 2), level=14),
    }


def test_recursive_bugs_automaton_tile_has_neighbor_from_level_below_if_on_inner_edge():
    automaton = RecursiveBugsAutomaton(width=5, height=5)

    tile = RecursiveTile(position=Vector2D(1, 2), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 8
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(1, 3), level=13),
        RecursiveTile(position=Vector2D(1, 1), level=13),
        RecursiveTile(position=Vector2D(0, 2), level=13),
        RecursiveTile(position=Vector2D(0, 0), level=12),
        RecursiveTile(position=Vector2D(0, 1), level=12),
        RecursiveTile(position=Vector2D(0, 2), level=12),
        RecursiveTile(position=Vector2D(0, 3), level=12),
        RecursiveTile(position=Vector2D(0, 4), level=12),
    }

    tile = RecursiveTile(position=Vector2D(3, 2), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 8
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(4, 2), level=13),
        RecursiveTile(position=Vector2D(3, 3), level=13),
        RecursiveTile(position=Vector2D(3, 1), level=13),
        RecursiveTile(position=Vector2D(4, 0), level=12),
        RecursiveTile(position=Vector2D(4, 1), level=12),
        RecursiveTile(position=Vector2D(4, 2), level=12),
        RecursiveTile(position=Vector2D(4, 3), level=12),
        RecursiveTile(position=Vector2D(4, 4), level=12),
    }

    tile = RecursiveTile(position=Vector2D(2, 1), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 8
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(3, 1), level=13),
        RecursiveTile(position=Vector2D(1, 1), level=13),
        RecursiveTile(position=Vector2D(2, 0), level=13),
        RecursiveTile(position=Vector2D(0, 0), level=12),
        RecursiveTile(position=Vector2D(1, 0), level=12),
        RecursiveTile(position=Vector2D(2, 0), level=12),
        RecursiveTile(position=Vector2D(3, 0), level=12),
        RecursiveTile(position=Vector2D(4, 0), level=12),
    }

    tile = RecursiveTile(position=Vector2D(2, 3), level=13)
    neighbors = list(automaton.neighbors(tile))
    assert len(neighbors) == 8
    assert set(neighbors) == {
        RecursiveTile(position=Vector2D(2, 4), level=13),
        RecursiveTile(position=Vector2D(3, 3), level=13),
        RecursiveTile(position=Vector2D(1, 3), level=13),
        RecursiveTile(position=Vector2D(0, 4), level=12),
        RecursiveTile(position=Vector2D(1, 4), level=12),
        RecursiveTile(position=Vector2D(2, 4), level=12),
        RecursiveTile(position=Vector2D(3, 4), level=12),
        RecursiveTile(position=Vector2D(4, 4), level=12),
    }


def test_recursive_bugs_automaton_can_advance_multiple_steps():
    initial_config_on_level_zero = {
        Vector2D(4, 0),
        Vector2D(0, 1),
        Vector2D(3, 1),
        Vector2D(0, 2),
        Vector2D(3, 2),
        Vector2D(4, 2),
        Vector2D(2, 3),
        Vector2D(0, 4),
    }
    automaton = RecursiveBugsAutomaton(width=5, height=5)
    final_configuration = automaton.advance(initial_config_on_level_zero, num_steps=10)
    assert len(final_configuration) == 99
