from typing import Optional
from models.cellular_automata import ElementaryAutomaton
from models.progress_bar_protocol import ProgressBar


def num_safe_tiles(
    first_row: str,
    num_rows: int,
    progress_bar: Optional[ProgressBar] = None,
) -> int:
    automaton = ElementaryAutomaton(rule=90)
    current_row = first_row.replace("^", "1").replace(".", "0")
    num_safe_tiles = current_row.count("0")
    for step in range(num_rows - 1):
        if progress_bar:
            progress_bar.update(step, num_rows)
        current_row = automaton.next_state(current_row)
        num_safe_tiles += current_row.count("0")
    return num_safe_tiles
