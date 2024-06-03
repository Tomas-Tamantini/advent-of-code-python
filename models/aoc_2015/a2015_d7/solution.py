from models.common.io import InputReader
from .parser import parse_logic_gates_circuit


def aoc_2015_d7(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 7: Some Assembly Required ---")
    circuit = parse_logic_gates_circuit(input_reader)
    a_value = circuit.get_value("a")
    print(f"Part 1: Wire a has signal of {a_value}")
    new_a_value = circuit.get_value("a", override_values={"b": a_value})
    print(f"Part 2: After b is overriden, wire a has signal of {new_a_value}")