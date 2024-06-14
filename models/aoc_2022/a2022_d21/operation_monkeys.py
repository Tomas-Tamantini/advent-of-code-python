from typing import Protocol, Callable
from dataclasses import dataclass, field


class OperationMonkey(Protocol):
    @property
    def name(self) -> str: ...

    def evaluate(self) -> int: ...


@dataclass
class LeafMonkey:
    name: str
    value: int

    def evaluate(self) -> int:
        return self.value


@dataclass
class BinaryOperationMonkey:
    left_child: OperationMonkey
    right_child: OperationMonkey
    operation: Callable[[int, int], int]

    def evaluate(self) -> int:
        return self.operation(self.left_child.evaluate(), self.right_child.evaluate())
