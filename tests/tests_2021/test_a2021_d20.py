from math import inf
from models.vectors import Vector2D
from models.aoc_2021 import TrenchMapAutomaton


def test_trench_map_automaton_with_empty_rule_set_returns_empty_set():
    automaton = TrenchMapAutomaton(
        lit_cell_configurations=set(),
    )
    next_state = automaton.next_state({Vector2D(1, 2): 1, Vector2D(2, 3): 1})
    lit_cells = {cell for cell, status in next_state.items() if status == 1}
    assert lit_cells == set()


def test_trench_map_automaton_considers_9_cells_surrounding_given_cell_and_turn_to_binary_number():
    automaton = TrenchMapAutomaton(
        lit_cell_configurations={0b000_010_000, 0b000_000_001},
    )
    next_state = automaton.next_state({Vector2D(10, 20): 1})
    lit_cells = {cell for cell, status in next_state.items() if status == 1}
    assert lit_cells == {Vector2D(10, 20), Vector2D(9, 19)}


def test_trench_map_automaton_can_run_multiple_steps():
    rules_as_str = (
        "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##"
        + "#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###"
        + ".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#."
        + ".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....."
        + ".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.."
        + "...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....."
        + "..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
    )
    lit_cell_configurations = {i for i, c in enumerate(rules_as_str) if c == "#"}
    initial_lit_cells = {
        Vector2D(0, 0),
        Vector2D(3, 0),
        Vector2D(0, 1),
        Vector2D(0, 2),
        Vector2D(1, 2),
        Vector2D(4, 2),
        Vector2D(2, 3),
        Vector2D(2, 4),
        Vector2D(3, 4),
        Vector2D(4, 4),
    }
    automaton = TrenchMapAutomaton(lit_cell_configurations)
    assert (
        automaton.num_lit_cells_after(num_steps=1, initial_lit_cells=initial_lit_cells)
        == 24
    )
    assert (
        automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=initial_lit_cells)
        == 35
    )


def test_trench_automaton_with_0_and_511_in_its_rules_has_infinite_lit_cells_from_first_iteration_forward():
    automaton = TrenchMapAutomaton(
        lit_cell_configurations={0b000_000_000, 0b111_111_111},
    )
    assert automaton.num_lit_cells_after(num_steps=0, initial_lit_cells=set()) == 0
    assert automaton.num_lit_cells_after(num_steps=1, initial_lit_cells=set()) == inf
    assert automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=set()) == inf


def test_trench_automaton_with_0_but_not_511_in_its_rules_has_infinite_lit_cells_on_odd_iterations():
    automaton = TrenchMapAutomaton(
        lit_cell_configurations={0b000_000_000},
    )
    assert automaton.num_lit_cells_after(num_steps=0, initial_lit_cells=set()) == 0
    assert automaton.num_lit_cells_after(num_steps=1, initial_lit_cells=set()) == inf
    assert automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=set()) == 0
    assert automaton.num_lit_cells_after(num_steps=3, initial_lit_cells=set()) == inf
