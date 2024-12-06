from queue import Queue
from typing import Iterable, Iterator

from .communication_modules import CommunicationModule
from .pulse import Pulse
from .pulse_monitor import PulseMonitor


class ModuleNetwork:
    def __init__(
        self,
        modules: Iterable[CommunicationModule],
        connections: dict[str, tuple[str, ...]],
    ) -> None:
        self._modules = {m.name: m for m in modules}
        self._connections = connections

    def _output_pulses(self, input_pulse: Pulse) -> Iterator[Pulse]:
        if module := self._modules.get(input_pulse.destination):
            if (output_pulse_type := module.propagate(input_pulse)) is not None:
                for destination in self._connections[module.name]:
                    yield Pulse(
                        origin=module.name,
                        destination=destination,
                        pulse_type=output_pulse_type,
                    )

    def propagate(self, initial_pulse: Pulse, monitor: PulseMonitor) -> None:
        pulse_queue = Queue()
        pulse_queue._put(initial_pulse)
        while not pulse_queue.empty():
            pulse = pulse_queue.get()
            monitor.track(pulse)
            for output_pulse in self._output_pulses(pulse):
                pulse_queue.put(output_pulse)

    def reset(self) -> None:
        for module in self._modules.values():
            module.reset()
