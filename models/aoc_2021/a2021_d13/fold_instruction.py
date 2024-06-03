from dataclasses import dataclass
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class FoldInstruction:
    is_horizontal_fold: bool
    line: int

    def _fold_along_horizontal_line(self, position: Vector2D) -> Vector2D:
        if position.y <= self.line:
            return position
        else:
            return Vector2D(position.x, 2 * self.line - position.y)

    def _fold_along_vertical_line(self, position: Vector2D) -> Vector2D:
        if position.x <= self.line:
            return position
        else:
            return Vector2D(2 * self.line - position.x, position.y)

    def _apply_to_single_position(self, position: Vector2D) -> Vector2D:
        if self.is_horizontal_fold:
            return self._fold_along_horizontal_line(position)
        else:
            return self._fold_along_vertical_line(position)

    def apply(self, positions: set[Vector2D]) -> set[Vector2D]:
        return {self._apply_to_single_position(p) for p in positions}
