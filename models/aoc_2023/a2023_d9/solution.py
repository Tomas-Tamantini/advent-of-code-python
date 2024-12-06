from typing import Iterator

from models.common.io import InputReader, IOHandler, Problem, ProblemSolution


def _difference(sequence: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1))


def _differences(sequence: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    yield sequence
    while len(set(sequence)) > 1:
        sequence = _difference(sequence)
        yield sequence


def next_in_sequence(sequence: tuple[int, ...]) -> int:
    differences = list(_differences(sequence))
    return sum(diff[-1] for diff in differences)


def previous_in_sequence(sequence: tuple[int, ...]) -> int:
    differences = list(_differences(sequence))
    return sum(diff[0] * (1 - 2 * (i % 2)) for i, diff in enumerate(differences))


def _parse_sequences(input_reader: InputReader) -> Iterator[tuple[int, ...]]:
    for line in input_reader.read_stripped_lines():
        yield tuple(map(int, line.split()))


def aoc_2023_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 9, "Mirage Maintenance")
    io_handler.output_writer.write_header(problem_id)
    sequences = tuple(_parse_sequences(io_handler.input_reader))
    extrapolate_forward = sum(next_in_sequence(sequence) for sequence in sequences)
    yield ProblemSolution(
        problem_id,
        f"The sum of values extrapolated forward is {extrapolate_forward}.",
        result=extrapolate_forward,
        part=1,
    )

    extrapolate_backward = sum(previous_in_sequence(sequence) for sequence in sequences)
    yield ProblemSolution(
        problem_id,
        f"The sum of values extrapolated backward is {extrapolate_backward}.",
        result=extrapolate_backward,
        part=2,
    )
