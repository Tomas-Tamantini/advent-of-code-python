from dataclasses import dataclass
from typing import Optional, Protocol

from .pulse import Pulse, PulseType


class CommunicationModule(Protocol):
    @property
    def name(self) -> str: ...

    def propagate(self, input_pulse: Pulse) -> Optional[PulseType]: ...

    def reset(self) -> None: ...


@dataclass(frozen=True)
class BroadcastModule:
    name: str

    @staticmethod
    def propagate(input_pulse: Pulse) -> Optional[PulseType]:
        return input_pulse.pulse_type

    def reset(self) -> None:
        pass


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

    def reset(self) -> None:
        self._is_on = False


class ConjunctionModule:
    def __init__(self, name: str, num_inputs: int) -> None:
        self._name = name
        self._high_inputs = set()
        self._num_inputs = num_inputs

    @property
    def num_high_inputs(self) -> int:
        return len(self._high_inputs)

    @property
    def name(self) -> str:
        return self._name

    def propagate(self, input_pulse: Pulse) -> Optional[PulseType]:
        if input_pulse.pulse_type == PulseType.HIGH:
            self._high_inputs.add(input_pulse.origin)
            return (
                PulseType.LOW
                if self.num_high_inputs == self._num_inputs
                else PulseType.HIGH
            )
        else:
            self._high_inputs.discard(input_pulse.origin)
            return PulseType.HIGH

    def reset(self) -> None:
        self._high_inputs = set()
