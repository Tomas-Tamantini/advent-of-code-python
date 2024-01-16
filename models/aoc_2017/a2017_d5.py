from typing import Iterator, Callable


def follow_and_increment_jump_instructions(
    jump_instructions: list[int], increment_rule: Callable[[int], int]
) -> Iterator[int]:
    current_pos = 0
    while 0 <= current_pos < len(jump_instructions):
        yield current_pos
        jump = jump_instructions[current_pos]
        jump_instructions[current_pos] = increment_rule(jump)
        current_pos += jump
