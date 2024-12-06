from dataclasses import dataclass
from typing import Iterator, Protocol

from models.common.vectors import Vector2D

from .ash_valley import AshValley
from .reflection_orientation import ReflectionOrientation


class LineOfReflection(Protocol):
    @property
    def line_index(self) -> int: ...

    @property
    def orientation(self) -> ReflectionOrientation: ...

    @classmethod
    def dimension(cls, valley: AshValley) -> int: ...

    def mirror_positions(
        self, valey: AshValley
    ) -> Iterator[tuple[Vector2D, Vector2D]]: ...


@dataclass(frozen=True)
class HorizontalLineOfReflection:
    line_index: int

    @property
    def orientation(self) -> ReflectionOrientation:
        return ReflectionOrientation.HORIZONTAL

    @classmethod
    def dimension(cls, valley: AshValley) -> int:
        return valley.height

    def mirror_positions(
        self, valley: AshValley
    ) -> Iterator[tuple[Vector2D, Vector2D]]:
        for offset in range(self.line_index + 1):
            reflected_row_index = self.line_index + offset + 1
            if reflected_row_index >= valley.height:
                break
            for col_index in range(valley.width):
                pos_a = Vector2D(col_index, self.line_index - offset)
                pos_b = Vector2D(col_index, reflected_row_index)
                yield pos_a, pos_b


@dataclass(frozen=True)
class VerticalLineOfReflection:
    line_index: int

    @classmethod
    def dimension(cls, valley: AshValley) -> int:
        return valley.width

    @property
    def orientation(self) -> ReflectionOrientation:
        return ReflectionOrientation.VERTICAL

    def mirror_positions(
        self, valley: AshValley
    ) -> Iterator[tuple[Vector2D, Vector2D]]:
        for offset in range(self.line_index + 1):
            reflected_col_index = self.line_index + offset + 1
            if reflected_col_index >= valley.width:
                break
            for row_index in range(valley.height):
                pos_a = Vector2D(self.line_index - offset, row_index)
                pos_b = Vector2D(reflected_col_index, row_index)
                yield pos_a, pos_b
