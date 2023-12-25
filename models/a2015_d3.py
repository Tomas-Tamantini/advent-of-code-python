def houses_with_at_least_one_present(instructions: str) -> set[tuple[int, int]]:
    visited_houses = {(0, 0)}
    current_x = 0
    current_y = 0
    for direction in instructions:
        if direction == "^":
            current_y += 1
        elif direction == "v":
            current_y -= 1
        elif direction == ">":
            current_x += 1
        elif direction == "<":
            current_x -= 1
        visited_houses.add((current_x, current_y))
    return visited_houses
