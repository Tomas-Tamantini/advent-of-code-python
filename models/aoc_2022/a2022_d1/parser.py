from typing import Iterator


def parse_calories(file_name: str) -> Iterator[tuple[int, ...]]:
    current_calories = []
    with open(file_name, "r") as file:
        for line in file:
            if line.strip():
                current_calories.append(int(line))
            elif current_calories:
                yield tuple(current_calories)
                current_calories.clear()
    if current_calories:
        yield tuple(current_calories)
