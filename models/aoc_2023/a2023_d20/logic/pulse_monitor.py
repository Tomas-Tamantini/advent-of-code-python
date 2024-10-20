from typing import Protocol
from .pulse import Pulse


class PulseMonitor(Protocol):
    def track(self, pulse: Pulse) -> None: ...
