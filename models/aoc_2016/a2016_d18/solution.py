from typing import Optional
from models.common.io import IOHandler, ProgressBar
from models.common.cellular_automata import ElementaryAutomaton


def num_safe_tiles(
    first_row: str,
    num_rows: int,
    progress_bar: Optional[ProgressBar] = None,
) -> int:
    automaton = ElementaryAutomaton(rule=90, min_idx=0, max_idx=len(first_row) - 1)
    current_state = {i for i, c in enumerate(first_row) if c == "^"}
    num_unsafe_tiles = len(current_state)
    for step in range(num_rows - 1):
        if progress_bar:
            progress_bar.update(step, num_rows)
        current_state = automaton.next_state(current_state)
        num_unsafe_tiles += len(current_state)
    return len(first_row) * num_rows - num_unsafe_tiles


def aoc_2016_d18(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2016, 18, "Like a Rogue")
    first_row = io_handler.input_reader.read().strip()
    num_safe = num_safe_tiles(first_row, num_rows=40)
    print(f"Part 1: Number of safe tiles in 40 rows: {num_safe}")
    num_safe = num_safe_tiles(
        first_row, num_rows=400_000, progress_bar=io_handler.progress_bar
    )
    print(f"Part 2: Number of safe tiles in 400000 rows: {num_safe}")
