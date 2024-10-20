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


class LowPulseMonitor:
    def __init__(self, modules_to_monitor: set[str]) -> None:
        self._modules_to_monitor = modules_to_monitor
        self._num_iterations_until_low_pulse = dict()
        self._total_iterations = 0

    def all_monitored_modules_received_low_pulse(self) -> bool:
        return len(self._num_iterations_until_low_pulse) == len(
            self._modules_to_monitor
        )

    def increment_iteration(self) -> None:
        self._total_iterations += 1

    def track(self, pulse: Pulse) -> None:
        if (
            (pulse.pulse_type == PulseType.LOW)
            and (pulse.destination in self._modules_to_monitor)
            and (pulse.destination not in self._num_iterations_until_low_pulse)
        ):
            self._num_iterations_until_low_pulse[pulse.destination] = (
                self._total_iterations
            )

    def num_iterations_until_first_low_pulse(self) -> dict[str, int]:
        return self._num_iterations_until_low_pulse
