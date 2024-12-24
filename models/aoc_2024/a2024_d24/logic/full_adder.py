from dataclasses import dataclass
from typing import Iterable, Iterator, Optional

from .circuit import Circuit
from .logic_gate import AndGate, LogicGate, XorGate

_INPUT_CHR = "x"
_OUTPUT_CHR = "z"


@dataclass(frozen=True)
class _FullAdder:
    input_xor: XorGate
    input_and: AndGate
    intermediate_xor: XorGate
    expected_out_wire: str

    def swapped_pair(self) -> Optional[tuple[str, str]]:
        if self.intermediate_xor.wire_output != self.expected_out_wire:
            return self.intermediate_xor.wire_output, self.expected_out_wire
        elif not self.intermediate_xor.has_input(self.input_xor.wire_output):
            return self.input_xor.wire_output, self.input_and.wire_output


def _input_gate_indices(circuit: Circuit) -> Iterator[int]:
    for gate in circuit.gates:
        if gate.wire_input_a.startswith(_INPUT_CHR) or gate.wire_input_b.startswith(
            _INPUT_CHR
        ):
            yield int(gate.wire_input_a[1:])


def _xor_gate(gates: Iterable[LogicGate]) -> XorGate:
    return next(g for g in gates if isinstance(g, XorGate))


def _and_gate(gates: Iterable[LogicGate]) -> AndGate:
    return next(g for g in gates if isinstance(g, AndGate))


def _build_full_adder(circuit: Circuit, full_adder_id: int) -> _FullAdder:
    input_id = f"{_INPUT_CHR}{full_adder_id:02}"
    output_id = f"{_OUTPUT_CHR}{full_adder_id:02}"
    input_xor = _xor_gate(circuit.gates_with_some_input(input_id))
    input_and = _and_gate(circuit.gates_with_some_input(input_id))
    intermediate_xor = _xor_gate(
        circuit.gates_with_some_input(input_and.wire_output, input_xor.wire_output)
    )
    return _FullAdder(input_xor, input_and, intermediate_xor, output_id)


def swapped_pair_of_wires_for_full_adder(circuit: Circuit) -> Iterator[set[str]]:
    num_full_adders = max(_input_gate_indices(circuit))
    for i in range(1, num_full_adders + 1):
        full_adder = _build_full_adder(circuit, i)
        if (swapped := full_adder.swapped_pair()) is not None:
            yield set(swapped)
