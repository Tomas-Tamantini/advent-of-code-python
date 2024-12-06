from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution


# Solved by manually parsing input code
def _offsets(
    x_offsets: list[int], y_offsets: list[int], is_largest: bool
) -> Iterator[int]:
    stack = []
    for i, (x_offset, y_offset) in enumerate(zip(x_offsets, y_offsets)):
        if x_offset > 0:
            stack.append((i, y_offset))
            continue
        j, new_y_offset = stack.pop()
        power_offset = (
            i
            if (is_largest and x_offset <= -new_y_offset)
            or (not is_largest and x_offset >= -new_y_offset)
            else j
        )
        power = 13 - power_offset
        yield abs((x_offset + new_y_offset) * 10**power)


def _largest_number_accepted_by_monad(
    x_offsets: list[int], y_offsets: list[int]
) -> int:
    return 99999999999999 - sum(_offsets(x_offsets, y_offsets, is_largest=True))


def _smallest_number_accepted_by_monad(
    x_offsets: list[int], y_offsets: list[int]
) -> int:
    return 11111111111111 + sum(_offsets(x_offsets, y_offsets, is_largest=False))


def aoc_2021_d24(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 24, "Arithmetic Logic Unit")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(io_handler.input_reader.readlines())
    x_offsets = [int(instructions[18 * i + 5].split()[-1]) for i in range(14)]
    y_offsets = [int(instructions[18 * i + 15].split()[-1]) for i in range(14)]
    largest = _largest_number_accepted_by_monad(x_offsets, y_offsets)
    yield ProblemSolution(
        problem_id,
        f"The largest number accepted by the monad is {largest}",
        part=1,
        result=largest,
    )

    smallest = _smallest_number_accepted_by_monad(x_offsets, y_offsets)
    yield ProblemSolution(
        problem_id,
        f"The smallest number accepted by the monad is {smallest}",
        part=2,
        result=smallest,
    )
