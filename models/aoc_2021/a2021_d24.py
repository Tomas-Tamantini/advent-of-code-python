# Solved by manually parsing input code

from typing import Iterator


def _offsets(
    x_offsets: list[int], y_offsets: list[int], is_largest: bool
) -> Iterator[int]:
    stack = []
    for i, (x_offset, y_offset) in enumerate(zip(x_offsets, y_offsets)):
        if x_offset > 0:
            stack.append((i, y_offset))
            continue
        j, y_offset = stack.pop()
        power_offset = (
            i
            if (is_largest and x_offset <= -y_offset)
            or (not is_largest and x_offset >= -y_offset)
            else j
        )
        power = 13 - power_offset
        yield abs((x_offset + y_offset) * 10**power)


def largest_number_accepted_by_monad(x_offsets: list[int], y_offsets: list[int]) -> int:
    return 99999999999999 - sum(_offsets(x_offsets, y_offsets, is_largest=True))


def smallest_number_accepted_by_monad(
    x_offsets: list[int], y_offsets: list[int]
) -> int:
    return 11111111111111 + sum(_offsets(x_offsets, y_offsets, is_largest=False))
