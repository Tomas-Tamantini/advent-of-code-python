from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import PacketParser


def aoc_2021_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 16, "Packet Decoder")
    io_handler.output_writer.write_header(problem_id)
    packet_as_hex = io_handler.input_reader.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    result = packet.version_sum()
    yield ProblemSolution(
        problem_id, f"The sum of all versions is {result}", result, part=1
    )
    result = packet.evaluate()
    yield ProblemSolution(
        problem_id, f"The evaluation of the packet is {result}", result, part=2
    )
