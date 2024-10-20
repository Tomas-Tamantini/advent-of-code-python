from typing import Iterator
from models.common.io import InputReader
from .logic import NetworkStep


def _parse_node_connections(line: str) -> tuple[str, str, str]:
    parts = line.split("=")
    node = parts[0].strip()
    neighbors = parts[1].replace("(", "").replace(")", "").split(",")
    left_neighbor = neighbors[0].strip()
    right_neighbor = neighbors[1].strip()
    return node, left_neighbor, right_neighbor


def parse_network_connections(input_reader: InputReader) -> dict[str, tuple[str, str]]:
    connections = dict()
    for line in input_reader.read_stripped_lines():
        if "=" in line:
            node, left_neighbor, right_neighbor = _parse_node_connections(line)
            connections[node] = left_neighbor, right_neighbor
    return connections


def parse_network_steps(input_reader: InputReader) -> Iterator[NetworkStep]:
    first_line = next(input_reader.read_stripped_lines())
    for character in first_line:
        yield {"R": NetworkStep.RIGHT, "L": NetworkStep.LEFT}[character]
