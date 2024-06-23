from collections import defaultdict
from models.common.io import IOHandler, Problem
from .parser import parse_line_segments


def aoc_2021_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 5, "Hydrothermal Venture")
    io_handler.output_writer.write_header(problem_id)
    segments = list(parse_line_segments(io_handler.input_reader))

    def num_overlapping_positions(segments):
        position_count = defaultdict(int)
        for segment in segments:
            for point in segment.all_points():
                position_count[point] += 1
        return sum(1 for count in position_count.values() if count > 1)

    non_diagonal_segments = [segment for segment in segments if not segment.is_diagonal]
    num_count = num_overlapping_positions(non_diagonal_segments)
    print(f"Part 1: The number of intersections of non-diagonals is {num_count}")

    num_count = num_overlapping_positions(segments)
    print(f"Part 2: The number of intersections of all segments is {num_count}")
