from models.common.io import InputReader

from .logic_gates import (
    AndGate,
    DoNothingGate,
    LeftShiftGate,
    LogicGatesCircuit,
    NotGate,
    OrGate,
    RightShiftGate,
)


def _parse_logic_gate_input(gate, input: str) -> None:
    try:
        input_signal = int(input)
        gate.add_input_signal(input_signal)
    except ValueError:
        gate.add_input_wire(input.strip())


def parse_logic_gates_circuit(input_reader: InputReader) -> LogicGatesCircuit:
    circuit = LogicGatesCircuit()
    for line in input_reader.readlines():
        if "->" not in line:
            continue
        input_str, output_str = line.split("->")
        output_wire = output_str.strip()
        if "AND" in input_str:
            gate = AndGate()
            inputs = input_str.split("AND")
        elif "OR" in input_str:
            gate = OrGate()
            inputs = input_str.split("OR")
        elif "LSHIFT" in input_str:
            input_wire_str, shift_str = input_str.split("LSHIFT")
            gate = LeftShiftGate(shift=int(shift_str), num_bits=16)
            inputs = [input_wire_str]
        elif "RSHIFT" in input_str:
            input_wire_str, shift_str = input_str.split("RSHIFT")
            gate = RightShiftGate(shift=int(shift_str), num_bits=16)
            inputs = [input_wire_str]
        elif "NOT" in input_str:
            gate = NotGate(num_bits=16)
            _, input_wire_str = input_str.split("NOT")
            inputs = [input_wire_str]
        else:
            gate = DoNothingGate()
            _parse_logic_gate_input(gate, input_str)
            inputs = [input_str]
        for input in inputs:
            _parse_logic_gate_input(gate, input)
        circuit.add_gate(gate, output_wire)
    return circuit
