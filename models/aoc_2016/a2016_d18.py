from typing import Optional
from models.cellular_automata import ElementaryAutomaton
from models.progress_bar_protocol import ProgressBar


def num_safe_tiles(
    first_row: str,
    num_rows: int,
    progress_bar: Optional[ProgressBar] = None,
) -> int:
    automaton = ElementaryAutomaton(rule=90)
    current_state = {i for i, c in enumerate(first_row) if c == "^"}
    num_unsafe_tiles = len(current_state)
    for step in range(num_rows - 1):
        if progress_bar:
            progress_bar.update(step, num_rows)
        current_state = automaton.next_state(
            current_state, min_idx=0, max_idx=len(first_row) - 1
        )
        num_unsafe_tiles += len(current_state)
    return len(first_row) * num_rows - num_unsafe_tiles
