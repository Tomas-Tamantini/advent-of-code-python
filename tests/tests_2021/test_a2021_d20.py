from models.vectors import Vector2D
from models.aoc_2021 import TrenchMapAutomaton


def test_trench_map_automaton_with_empty_rule_set_returns_empty_set():
    automaton = TrenchMapAutomaton(
        live_cell_configurations=set(),
    )
    assert automaton.next_state({Vector2D(1, 2), Vector2D(2, 3)}) == set()


def test_trench_map_automaton_considers_9_cells_surrounding_given_cell_and_turn_to_binary_number():
    automaton = TrenchMapAutomaton(
        live_cell_configurations={0b000_010_000, 0b000_000_001},
    )
    assert automaton.next_state({Vector2D(10, 20)}) == {
        Vector2D(10, 20),
        Vector2D(9, 19),
    }


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
    live_cell_configurations = {i for i, c in enumerate(rules_as_str) if c == "#"}
    initial_state = {
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
    automaton = TrenchMapAutomaton(live_cell_configurations)
    state_after_one_step = automaton.multi_step(initial_state, 1)
    assert len(state_after_one_step) == 24
    state_after_two_steps = automaton.multi_step(initial_state, 2)
    assert len(state_after_two_steps) == 35
