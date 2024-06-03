from models.common.io import InputReader, ProgressBarConsole
from .parser import parse_trench_rules_and_trench_map
from .trench_map_automaton import TrenchMapAutomaton


def aoc_2021_d20(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2021 - Day 20: Trench Map ---")
    lit_cell_configurations, lit_cells = parse_trench_rules_and_trench_map(input_reader)
    automaton = TrenchMapAutomaton(lit_cell_configurations)
    num_lit = automaton.num_lit_cells_after(num_steps=2, initial_lit_cells=lit_cells)
    print(f"Part 1: The number of lit cells after two steps is {num_lit}")
    num_lit = automaton.num_lit_cells_after(
        num_steps=50, initial_lit_cells=lit_cells, progress_bar=progress_bar
    )
    print(f"Part 2: The number of lit cells after 50 steps is {num_lit}")
