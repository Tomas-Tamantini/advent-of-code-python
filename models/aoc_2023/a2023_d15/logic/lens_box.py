from typing import Iterator
from .lens import Lens


class LensBox:
    def __init__(self) -> None:
        self._lenses = []

    def lenses(self) -> Iterator[Lens]:
        yield from self._lenses

    def remove_lens(self, lens_label: str) -> None:
        for i, lens in enumerate(self._lenses):
            if lens.label == lens_label:
                del self._lenses[i]

    def insert_lens(self, lens: Lens) -> None:
        for i, previous_lens in enumerate(self._lenses):
            if previous_lens.label == lens.label:
                self._lenses[i] = lens
                return
        self._lenses.append(lens)
