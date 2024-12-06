from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .bugs_automaton import BugsAutomaton, RecursiveBugsAutomaton


def aoc_2019_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 24, "Planet of Discord")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    live_cells = set(grid.positions_with_value("#"))

    automaton = BugsAutomaton(width=5, height=5)
    repeated_state = automaton.first_pattern_to_appear_twice(live_cells)
    rating = automaton.biodiversity_rating(repeated_state)
    yield ProblemSolution(
        problem_id,
        f"Biodiversity rating of the first repeated state is {rating}",
        part=1,
        result=rating,
    )

    recursive_automaton = RecursiveBugsAutomaton(width=5, height=5)
    final_state = recursive_automaton.advance(
        initial_configuration_on_level_zero=live_cells,
        num_steps=200,
        progress_bar=io_handler.progress_bar,
    )
    num_bugs = len(final_state)
    yield ProblemSolution(
        problem_id,
        f"Number of bugs in recursive grid after 200 minutes is {num_bugs}",
        part=2,
        result=num_bugs,
    )
