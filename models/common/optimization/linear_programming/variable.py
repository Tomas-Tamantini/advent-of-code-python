from typing import Hashable, Protocol
from dataclasses import dataclass
from math import inf


VariableId = Hashable


class VariableProtocol(Protocol):
    @property
    def variable_id(self) -> VariableId: ...

    @property
    def description(self) -> str: ...

    @property
    def lower_bound(self) -> float: ...

    @property
    def upper_bound(self) -> float: ...

    @property
    def is_integer(self) -> bool: ...


@dataclass(frozen=True)
class ContinuousVariable:
    id: VariableId
    description: str = ""
    lower_bound: float = 0
    upper_bound: float = inf

    @property
    def is_integer(self) -> bool:
        return False


@dataclass(frozen=True)
class IntegerVariable:
    id: VariableId
    description: str = ""
    lower_bound: float = 0
    upper_bound: float = inf

    @property
    def is_integer(self) -> bool:
        return True


@dataclass(frozen=True)
class BinaryVariable:
    id: VariableId
    description: str = ""

    @property
    def lower_bound(self) -> float:
        return 0

    @property
    def upper_bound(self) -> float:
        return 1

    @property
    def is_integer(self) -> bool:
        return True
