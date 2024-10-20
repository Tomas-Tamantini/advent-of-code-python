from dataclasses import dataclass
from typing import Optional, Protocol
from .pulse import Pulse, PulseType


class CommunicationModule(Protocol):
    @property
    def name(self) -> str: ...

    def propagate(self, input_pulse: Pulse) -> Optional[PulseType]: ...


@dataclass(frozen=True)
class BroadcastModule:
    name: str

    def propagate(self, input_pulse: Pulse) -> Optional[PulseType]:
        return input_pulse.pulse_type


class FlipFlopModule:
    def __init__(self, name: str) -> None:
        self._name = name
        self._is_on = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool:
        return self._is_on

    def propagate(self, input_pulse: Pulse) -> Optional[PulseType]:
        if input_pulse.pulse_type == PulseType.LOW:
            self._is_on = not self._is_on
            return PulseType.HIGH if self._is_on else PulseType.LOW
