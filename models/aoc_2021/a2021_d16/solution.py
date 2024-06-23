from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import PacketParser


def aoc_2021_d16(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 16, "Packet Decoder")
    io_handler.output_writer.write_header(problem_id)
    packet_as_hex = io_handler.input_reader.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    solution = ProblemSolution(
        problem_id, f"The sum of all versions is { packet.version_sum()}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id, f"The evaluation of the packet is { packet.evaluate()}", part=2
    )
    io_handler.output_writer.write_solution(solution)
