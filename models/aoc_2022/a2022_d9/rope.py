from dataclasses import dataclass
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class Rope:
    head: Vector2D = Vector2D(0, 0)
    tail_to_head: Vector2D = Vector2D(0, 0)

    @property
    def tail(self) -> Vector2D:
        return self.head - self.tail_to_head

    @staticmethod
    def _draw_closer(coordinate: int) -> int:
        if coordinate >= 0:
            return coordinate // 2
        else:
            return (coordinate + 1) // 2

    def move_head(self, direction: Vector2D) -> "Rope":
        new_tail_to_head = self.tail_to_head.move(direction)
        if abs(new_tail_to_head.x) > 1 or abs(new_tail_to_head.y) > 1:
            new_tail_to_head = Vector2D(
                self._draw_closer(new_tail_to_head.x),
                self._draw_closer(new_tail_to_head.y),
            )
        return Rope(
            head=self.head.move(direction),
            tail_to_head=new_tail_to_head,
        )
