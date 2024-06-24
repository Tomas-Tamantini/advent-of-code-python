from models.common.io import IOHandler, Problem, ProblemSolution
from .ip_parser import IpParser


def aoc_2016_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 7, "Internet Protocol Version 7")
    io_handler.output_writer.write_header(problem_id)
    num_ips_that_support_tls = 0
    num_ips_that_support_ssl = 0
    for line in io_handler.input_reader.readlines():
        ip_parser = IpParser(line.strip())
        if ip_parser.supports_tls():
            num_ips_that_support_tls += 1
        if ip_parser.supports_ssl():
            num_ips_that_support_ssl += 1
    solution = ProblemSolution(
        problem_id,
        f"Number of IPs that support TLS: {num_ips_that_support_tls}",
        part=1,
        result=num_ips_that_support_tls,
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Number of IPs that support SSL: {num_ips_that_support_ssl}",
        part=2,
        result=num_ips_that_support_ssl,
    )
    io_handler.set_solution(solution)
