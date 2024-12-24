from typing import Iterator

from models.common.io import InputReader

from .logic import AndGate, LogicGate, OrGate, Pulse, PulseType, XorGate


def _parse_logic_gate(line: str) -> LogicGate:
    parts = line.split(" ")
    wire_input_a = parts[0]
    wire_input_b = parts[2]
    wire_output = parts[-1]
    if parts[1] == "AND":
        return AndGate(wire_input_a, wire_input_b, wire_output)
    elif parts[1] == "OR":
        return OrGate(wire_input_a, wire_input_b, wire_output)
    elif parts[1] == "XOR":
        return XorGate(wire_input_a, wire_input_b, wire_output)
    else:
        raise ValueError(f"Unknown logic gate: {line}")


def parse_logic_gates(input_reader: InputReader) -> Iterator[LogicGate]:
    for line in input_reader.read_stripped_lines():
        if "->" in line:
            yield _parse_logic_gate(line)


def parse_input_pulses(input_reader: InputReader) -> Iterator[Pulse]:
    for line in input_reader.read_stripped_lines():
        if ":" in line:
            wire, value = line.split(":")
            pulse_type = PulseType.HIGH if value.strip() == "1" else PulseType.LOW
            yield Pulse(wire, pulse_type)
