from typing import Protocol, Iterator
from .pulse import Pulse, PulseType


class PulseMonitor(Protocol):
    def track(self, pulse: Pulse) -> None: ...


class PulseHistory:
    def __init__(self) -> None:
        self._history = []

    def history(self) -> Iterator[Pulse]:
        yield from self._history

    def track(self, pulse: Pulse) -> None:
        self._history.append(pulse)


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
