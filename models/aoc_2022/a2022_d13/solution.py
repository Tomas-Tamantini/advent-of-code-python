from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .packet_comparison import left_packet_leq_right


def aoc_2022_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 13, "Distress Signal")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.read_stripped_lines())
    sum_pair_indices = 0
    for pair_index in range(len(lines) // 2):
        packet_left = eval(lines[2 * pair_index])
        packet_right = eval(lines[2 * pair_index + 1])
        if left_packet_leq_right(packet_left, packet_right):
            sum_pair_indices += pair_index + 1
    yield ProblemSolution(
        problem_id,
        f"Sum of pair indices is {sum_pair_indices}",
        part=1,
        result=sum_pair_indices,
    )

    first_divider = [[2]]
    num_leq_first_divider = sum(
        left_packet_leq_right(eval(line), first_divider) for line in lines
    )
    second_divider = [[6]]
    num_leq_second_divider = sum(
        left_packet_leq_right(eval(line), second_divider) for line in lines
    )
    result = (num_leq_first_divider + 1) * (num_leq_second_divider + 2)
    yield ProblemSolution(
        problem_id, f"Product of divider indices is {result}", result, part=2
    )
