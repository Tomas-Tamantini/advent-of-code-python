from typing import Iterable, Optional


class _LogicGate:
    def __init__(self) -> None:
        self._inputs: list[str | int] = list()

    def add_input_wire(self, wire: str) -> None:
        self._inputs.append(wire)

    def add_input_signal(self, signal_value: int) -> None:
        self._inputs.append(signal_value)

    @property
    def input_wires(self) -> Iterable[str]:
        return (i for i in self._inputs if isinstance(i, str))

    def evaluate(self, input_signals: Optional[dict[str, int]] = None) -> int:
        if not input_signals:
            input_signals = dict()
        all_input_signals = [
            (i if isinstance(i, int) else input_signals[i]) for i in self._inputs
        ]
        return self._process_input_signals(all_input_signals)

    def _process_input_signals(self, signals: list[int]) -> int:
        raise NotImplementedError("Should be implemented by sub-classes")


class DoNothingGate(_LogicGate):
    def _process_input_signals(self, signals: list[int]) -> int:
        return signals[0]


class AndGate(_LogicGate):
    def _process_input_signals(self, signals: list[int]) -> int:
        return signals[0] & signals[1]


class OrGate(_LogicGate):
    def _process_input_signals(self, signals: list[int]) -> int:
        return signals[0] | signals[1]


class LeftShiftGate(_LogicGate):
    def __init__(self, shift: int, num_bits: int) -> None:
        super().__init__()
        self._num_bits = num_bits
        self._shift = shift

    def _process_input_signals(self, signals: list[int]) -> int:
        max_value = 2**self._num_bits
        return (signals[0] << self._shift) % max_value


class RightShiftGate(_LogicGate):
    def __init__(self, shift: int, num_bits: int) -> None:
        super().__init__()
        self._num_bits = num_bits
        self._shift = shift

    def _process_input_signals(self, signals: list[int]) -> int:
        max_value = 2**self._num_bits
        return (signals[0] % max_value) >> self._shift


class NotGate(_LogicGate):
    def __init__(self, num_bits: int) -> None:
        super().__init__()
        self._num_bits = num_bits

    def _process_input_signals(self, signals: list[int]) -> int:
        return 2**self._num_bits - 1 - signals[0]


class LogicGatesCircuit:
    def __init__(self) -> None:
        self._gates = dict()
        self._wire_values = dict()

    def add_gate(self, gate: _LogicGate, output_wire: str) -> None:
        if output_wire in self._gates:
            raise ValueError(f"Wire {output_wire} is already output of another gate")
        self._gates[output_wire] = gate

    def get_value(self, wire: str) -> int:
        wire_values = dict()
        return self._get_value_recursive(wire, wire_values)

    def _get_value_recursive(self, wire: str, wire_values: dict[str, int]) -> int:
        if wire in wire_values:
            return wire_values[wire]

        input_values = dict()
        for input_wire in self._gates[wire].input_wires:
            input_values[input_wire] = self._get_value_recursive(
                input_wire, wire_values
            )

        wire_value = self._gates[wire].evaluate(input_values)
        wire_values[wire] = wire_value
        return wire_value
