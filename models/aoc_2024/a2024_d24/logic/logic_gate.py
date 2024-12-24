from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class LogicGate(ABC):
    wire_input_a: str
    wire_input_b: str
    wire_output: str


@dataclass(frozen=True)
class AndGate(LogicGate): ...


@dataclass(frozen=True)
class OrGate(LogicGate): ...


@dataclass(frozen=True)
class XorGate(LogicGate): ...
