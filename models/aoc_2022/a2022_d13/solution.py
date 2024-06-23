from models.common.io import IOHandler
from .packet_comparison import left_packet_leq_right


def aoc_2022_d13(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2022, 13, "Distress Signal")
    lines = list(io_handler.input_reader.read_stripped_lines())
    sum_pair_indices = 0
    for pair_index in range(len(lines) // 2):
        packet_left = eval(lines[2 * pair_index])
        packet_right = eval(lines[2 * pair_index + 1])
        if left_packet_leq_right(packet_left, packet_right):
            sum_pair_indices += pair_index + 1
    print(f"Part 1: Sum of pair indices is {sum_pair_indices}")
    first_divider = [[2]]
    num_leq_first_divider = sum(
        left_packet_leq_right(eval(line), first_divider) for line in lines
    )
    second_divider = [[6]]
    num_leq_second_divider = sum(
        left_packet_leq_right(eval(line), second_divider) for line in lines
    )
    product = (num_leq_first_divider + 1) * (num_leq_second_divider + 2)
    print(f"Part 2: Product of divider indices is {product}")
