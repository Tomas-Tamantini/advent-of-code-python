from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import (
    MonitorBadAddressPackets,
    MonitorRepeatedYValuePackets,
    LostPackets,
    run_network,
)


def aoc_2019_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2019, 23, "Category Six")
    io_handler.output_writer.write_header(problem_id)
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    num_computers = 50
    lost_packets_manager = LostPackets(monitor=MonitorBadAddressPackets())
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y
    solution = ProblemSolution(
        problem_id, f"Y value of the first packet sent to address 255 is {ans}", part=1
    )
    io_handler.output_writer.write_solution(solution)

    lost_packets_manager = LostPackets(
        monitor=MonitorRepeatedYValuePackets(max_repeated_y=1)
    )
    io_handler.output_writer.give_time_estimation("1min", part=2)
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y

    solution = ProblemSolution(
        problem_id,
        f"Y value of the first packet sent to address 255 after NAT repeats a packet is {ans}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
