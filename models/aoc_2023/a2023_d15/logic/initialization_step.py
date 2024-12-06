from dataclasses import dataclass
from typing import Protocol

from .lens import Lens
from .lens_box import LensBox


class InitializationStep(Protocol):
    def __str__(self) -> str: ...

    @property
    def label(self) -> str: ...

    def apply(self, lens_box: LensBox) -> None: ...


@dataclass(frozen=True)
class RemoveLens:
    label: str

    def __str__(self) -> str:
        return f"{self.label}-"

    def apply(self, lens_box: LensBox) -> None:
        lens_box.remove_lens(self.label)


@dataclass(frozen=True)
class InsertLens:
    lens: Lens

    @property
    def label(self) -> str:
        return self.lens.label

    def __str__(self) -> str:
        return f"{self.lens.label}={self.lens.focal_strength}"

    def apply(self, lens_box: LensBox) -> None:
        lens_box.insert_lens(self.lens)
