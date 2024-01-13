from models.cellular_automata import ElementaryAutomaton


def num_safe_tiles(first_row: str, num_rows: int) -> int:
    automaton = ElementaryAutomaton(rule=90)
    current_row = first_row.replace("^", "1").replace(".", "0")
    num_safe_tiles = current_row.count("0")
    for _ in range(num_rows - 1):
        current_row = automaton.next_state(current_row)
        num_safe_tiles += current_row.count("0")
    return num_safe_tiles
