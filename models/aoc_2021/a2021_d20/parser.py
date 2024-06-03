from models.common.io import InputReader
from models.common.vectors import Vector2D


def parse_trench_rules_and_trench_map(
    input_reader: InputReader,
) -> tuple[set[int], set[Vector2D]]:
    trench_rules = set()
    trench_map = set()
    current_row = 0
    for line in input_reader.read_stripped_lines():
        active_columns = {i for i, c in enumerate(line) if c == "#"}
        if not trench_rules:
            trench_rules = active_columns
        else:
            trench_map.update(Vector2D(i, current_row) for i in active_columns)
            current_row += 1
    return trench_rules, trench_map
