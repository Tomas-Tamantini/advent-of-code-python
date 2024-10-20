from typing import Protocol
from .pulse import Pulse, PulseType


class PulseMonitor(Protocol):
    def track(self, pulse: Pulse) -> None: ...


class PulseCounter:
    def __init__(self) -> None:
        self._num_high = 0
        self._num_low = 0

    @property
    def num_high_pulses(self) -> int:
        return self._num_high

    @property
    def num_low_pulses(self) -> int:
        return self._num_low

    def track(self, pulse: Pulse) -> None:
        if pulse.pulse_type == PulseType.HIGH:
            self._num_high += 1
        else:
            self._num_low += 1
