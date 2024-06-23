from models.common.io import IOHandler, Problem
from .disjoint_intervals import DisjoinIntervals


def aoc_2016_d20(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 20, "Firewall Rules")
    io_handler.output_writer.write_header(problem_id)
    disjoint_intervals = DisjoinIntervals(0, 4_294_967_295)
    for line in io_handler.input_reader.readlines():
        start, end = map(int, line.strip().split("-"))
        disjoint_intervals.remove(start, end)
    lowest_allowed_ip = next(disjoint_intervals.intervals())[0]
    print(f"Part 1: Lowest allowed IP: {lowest_allowed_ip}")
    num_allowed_ips = disjoint_intervals.num_elements()
    print(f"Part 2: Number of allowed IPs: {num_allowed_ips}")
