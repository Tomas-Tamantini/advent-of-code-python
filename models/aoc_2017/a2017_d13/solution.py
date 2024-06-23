from models.common.io import IOHandler
from .parser import parse_layered_firewall


def aoc_2017_d13(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2017 - Day 13: Packet Scanners ---")
    firewall = parse_layered_firewall(io_handler.input_reader)
    packet_collisions = list(firewall.packet_collisions())
    severity = sum(
        layer_depth * layer.scanning_range for layer_depth, layer in packet_collisions
    )
    print(f"Part 1: Severity of packet collisions: {severity}")
    minimum_delay = firewall.minimum_delay_to_avoid_collisions()
    print(f"Part 2: Minimum delay to avoid collisions: {minimum_delay}")
