from models.common.io import IOHandler, Problem, ProblemSolution
from .disjoint_intervals import DisjoinIntervals


def aoc_2016_d20(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 20, "Firewall Rules")
    io_handler.output_writer.write_header(problem_id)
    disjoint_intervals = DisjoinIntervals(0, 4_294_967_295)
    for line in io_handler.input_reader.readlines():
        start, end = map(int, line.strip().split("-"))
        disjoint_intervals.remove(start, end)
    lowest_allowed_ip = next(disjoint_intervals.intervals())[0]
    solution = ProblemSolution(
        problem_id, f"Lowest allowed IP: {lowest_allowed_ip}", part=1
    )
    io_handler.set_solution(solution)
    num_allowed_ips = disjoint_intervals.num_elements()
    solution = ProblemSolution(
        problem_id, f"Number of allowed IPs: {num_allowed_ips}", part=2
    )
    io_handler.set_solution(solution)
