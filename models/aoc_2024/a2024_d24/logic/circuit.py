from collections import defaultdict
from typing import Iterable, Iterator

from .logic_gate import LogicGate
from .pulse import Pulse


class Circuit:
    def __init__(self, gates: Iterable[LogicGate]):
        self._gates = gates
        self._gates_with_input = defaultdict(list)
        for gate in gates:
            self._gates_with_input[gate.wire_input_a].append(gate)
            self._gates_with_input[gate.wire_input_b].append(gate)

    def propagate(self, pulses: Iterable[Pulse]) -> Iterator[Pulse]:
        pulse_stack = [p for p in pulses]
        stored_inputs = defaultdict(list)
        while pulse_stack:
            current_pulse = pulse_stack.pop()
            yield current_pulse
            for gate in self._gates_with_input[current_pulse.wire]:
                stored_inputs[gate].append(current_pulse.pulse_type)
                if len(stored_inputs[gate]) == 2:
                    pulse_stack.append(gate.output(*stored_inputs[gate]))
