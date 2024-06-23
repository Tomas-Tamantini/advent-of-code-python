from models.common.io import IOHandler, CharacterGrid
from .bugs_automaton import BugsAutomaton, RecursiveBugsAutomaton


def aoc_2019_d24(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 24: Planet of Discord ---")
    grid = CharacterGrid(io_handler.input_reader.read())
    live_cells = set(grid.positions_with_value("#"))

    automaton = BugsAutomaton(width=5, height=5)
    repeated_state = automaton.first_pattern_to_appear_twice(live_cells)
    rating = automaton.biodiversity_rating(repeated_state)
    print(f"Part 1: Biodiversity rating of the first repeated state is {rating}")

    recursive_automaton = RecursiveBugsAutomaton(width=5, height=5)
    final_state = recursive_automaton.advance(
        initial_configuration_on_level_zero=live_cells,
        num_steps=200,
        progress_bar=io_handler.progress_bar,
    )
    num_bugs = len(final_state)
    print(f"Part 2: Number of bugs in recursive grid after 200 minutes is {num_bugs}")
