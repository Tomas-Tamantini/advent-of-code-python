from typing import Protocol
from .hardware import Hardware


class Instruction(Protocol):
    def execute(self, hardware: Hardware) -> None:
        ...
