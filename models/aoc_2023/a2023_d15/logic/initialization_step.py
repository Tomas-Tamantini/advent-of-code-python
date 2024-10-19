from typing import Protocol
from dataclasses import dataclass


class InitializationStep(Protocol):

    def __str__(self) -> str: ...

    @property
    def label(self) -> str: ...


@dataclass(frozen=True)
class RemoveLens:
    label: str

    def __str__(self) -> str:
        return f"{self.label}-"


@dataclass(frozen=True)
class InsertLens:
    label: str
    focal_strength: int

    def __str__(self) -> str:
        return f"{self.label}={self.focal_strength}"
