from typing import Iterable, Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .circular_encryption import mix_list


def _numbers_at_offsets(numbers: list[int], offsets: Iterable[int]) -> Iterator[int]:
    zero_index = numbers.index(0)
    for offset in offsets:
        yield numbers[(zero_index + offset) % len(numbers)]


def aoc_2022_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 20, "Grove Positioning System")
    io_handler.output_writer.write_header(problem_id)
    offsets = (1000, 2000, 3000)
    numbers = [int(line) for line in io_handler.input_reader.read_stripped_lines()]
    shuffled_numbers = mix_list(numbers)
    total_sum = sum(_numbers_at_offsets(shuffled_numbers, offsets))
    yield ProblemSolution(
        problem_id,
        f"Sum of numbers at positions 1000, 2000, and 3000: {total_sum}",
        part=1,
        result=total_sum,
    )

    key = 811589153
    multiplied_list = [number * key for number in numbers]
    shuffled_multiplied_list = mix_list(
        multiplied_list, num_rounds=10, progress_bar=io_handler.progress_bar
    )
    total_sum = sum(_numbers_at_offsets(shuffled_multiplied_list, offsets))
    yield ProblemSolution(
        problem_id,
        (
            f"Sum of numbers at positions 1000, 2000, and 3000 "
            f"after 10 rounds mixing: {total_sum}"
        ),
        part=2,
        result=total_sum,
    )
