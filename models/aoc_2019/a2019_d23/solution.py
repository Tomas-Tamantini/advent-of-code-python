from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import (
    LostPackets,
    MonitorBadAddressPackets,
    MonitorRepeatedYValuePackets,
    run_network,
)


def aoc_2019_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 23, "Category Six")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    num_computers = 50
    lost_packets_manager = LostPackets(monitor=MonitorBadAddressPackets())
    run_network(num_computers, lost_packets_manager, instructions)
    result = lost_packets_manager.content_last_packet.y
    yield ProblemSolution(
        problem_id,
        f"Y value of the first packet sent to address 255 is {result}",
        result,
        part=1,
    )

    lost_packets_manager = LostPackets(
        monitor=MonitorRepeatedYValuePackets(max_repeated_y=1)
    )
    io_handler.output_writer.give_time_estimation("1min", part=2)
    run_network(num_computers, lost_packets_manager, instructions)
    result = lost_packets_manager.content_last_packet.y

    yield ProblemSolution(
        problem_id,
        (
            "Y value of the first packet sent to address 255 "
            f"after NAT repeats a packet is {result}"
        ),
        result,
        part=2,
    )
