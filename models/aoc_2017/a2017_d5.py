from typing import Iterator


def follow_and_increment_jump_instructions(
    jump_instructions: list[int],
) -> Iterator[int]:
    current_pos = 0
    while 0 <= current_pos < len(jump_instructions):
        yield current_pos
        jump = jump_instructions[current_pos]
        jump_instructions[current_pos] += 1
        current_pos += jump
