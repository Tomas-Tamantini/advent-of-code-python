from abc import ABC, abstractmethod
from dataclasses import dataclass

from .pulse import Pulse, PulseType


@dataclass(frozen=True)
class LogicGate(ABC):
    wire_input_a: str
    wire_input_b: str
    wire_output: str

    def has_input(self, wire_id: str) -> bool:
        return wire_id in {self.wire_input_a, self.wire_input_b}

    def output(self, signal_a: PulseType, signal_b: PulseType) -> Pulse:
        out_signal = self._output_level(signal_a, signal_b)
        return Pulse(self.wire_output, out_signal)

    @abstractmethod
    def _output_level(self, signal_a: PulseType, signal_b: PulseType) -> PulseType: ...


@dataclass(frozen=True)
class AndGate(LogicGate):
    @staticmethod
    def _output_level(signal_a: PulseType, signal_b: PulseType) -> PulseType:
        return (
            PulseType.HIGH if signal_a == signal_b == PulseType.HIGH else PulseType.LOW
        )


@dataclass(frozen=True)
class OrGate(LogicGate):
    @staticmethod
    def _output_level(signal_a: PulseType, signal_b: PulseType) -> PulseType:
        return (
            PulseType.HIGH if PulseType.HIGH in {signal_a, signal_b} else PulseType.LOW
        )


@dataclass(frozen=True)
class XorGate(LogicGate):
    @staticmethod
    def _output_level(signal_a: PulseType, signal_b: PulseType) -> PulseType:
        return PulseType.HIGH if signal_a != signal_b else PulseType.LOW
