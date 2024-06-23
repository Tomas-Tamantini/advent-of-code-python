from models.common.io import IOHandler
from .logic import PacketParser


def aoc_2021_d16(io_handler: IOHandler) -> None:
    print("--- AOC 2021 - Day 16: Packet Decoder ---")
    packet_as_hex = io_handler.input_reader.read().strip()
    packet = PacketParser().parse_packet(packet_as_hex)
    print(f"Part 1: The sum of all versions is { packet.version_sum()}")
    print(f"Part 2: The evaluation of the packet is { packet.evaluate()}")
