from typing import Protocol, Callable
from dataclasses import dataclass


class Packet(Protocol):
    @property
    def version_number(self) -> int: ...

    def evaluate(self) -> int: ...

    def version_sum(self) -> int: ...


@dataclass(frozen=True)
class LiteralPacket:
    version_number: int
    literal_value: int

    def evaluate(self) -> int:
        return self.literal_value

    def version_sum(self) -> int:
        return self.version_number


@dataclass(frozen=True)
class RecursivePacket:
    version_number: int
    subpackets: tuple[Packet, ...]
    operation: Callable[[tuple[int]], int]

    def evaluate(self) -> int:
        return self.operation(tuple(packet.evaluate() for packet in self.subpackets))

    def version_sum(self) -> int:
        return self.version_number + sum(
            packet.version_sum() for packet in self.subpackets
        )
