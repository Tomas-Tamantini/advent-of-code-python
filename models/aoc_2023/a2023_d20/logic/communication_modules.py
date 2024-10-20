from typing import Iterator, Protocol
from .pulse import Pulse, PulseType


class CommunicationModule(Protocol):
    @property
    def name(self) -> str: ...

    def propagate(self, pulse: Pulse) -> Iterator[Pulse]: ...


class FlipFlopModule:
    def __init__(self, name: str, output_module_name: str) -> None:
        self._name = name
        self._output_module_name = output_module_name
        self._is_on = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_on(self) -> bool:
        return self._is_on

    def propagate(self, pulse: Pulse) -> Iterator[Pulse]:
        if pulse.pulse_type == PulseType.LOW:
            self._is_on = not self._is_on
            output_type = PulseType.HIGH if self._is_on else PulseType.LOW
            yield Pulse(self._name, self._output_module_name, output_type)
