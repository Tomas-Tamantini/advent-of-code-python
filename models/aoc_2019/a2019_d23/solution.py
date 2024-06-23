from models.common.io import IOHandler
from .logic import (
    MonitorBadAddressPackets,
    MonitorRepeatedYValuePackets,
    LostPackets,
    run_network,
)


def aoc_2019_d23(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 23: Category Six ---")
    instructions = [int(code) for code in io_handler.input_reader.read().split(",")]
    num_computers = 50
    lost_packets_manager = LostPackets(monitor=MonitorBadAddressPackets())
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y
    print(f"Part 1: Y value of the first packet sent to address 255 is {ans}")

    lost_packets_manager = LostPackets(
        monitor=MonitorRepeatedYValuePackets(max_repeated_y=1)
    )
    print("Be patient, it takes ~1min to run", end="\r")
    run_network(num_computers, lost_packets_manager, instructions)
    ans = lost_packets_manager.content_last_packet.y

    print(
        f"Part 2: Y value of the first packet sent to address 255 after NAT repeats a packet is {ans}"
    )
