def final_floor(instructions: str) -> int:
    return instructions.count("(") - instructions.count(")")


def first_basement(instructions: str) -> int:
    floor = 0
    for i, c in enumerate(instructions, 1):
        floor += 1 if c == "(" else -1
        if floor == -1:
            return i
    return -1
