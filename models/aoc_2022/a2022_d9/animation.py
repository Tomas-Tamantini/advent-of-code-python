from models.common.vectors import Vector2D

from .logic import Rope


class RopeAnimation:
    def __init__(self, width: int, height: int, rope: Rope, total_num_iterations: int):
        self._width = width
        self._height = height
        self._focus_length = min(width, height) // 4
        self._head_to_tail = list(rope.positions_head_to_tail())
        self._center = self._head_position
        self._iteration = 0
        self._visited_by_tail = {rope.tail_position}
        self._total_num_iterations = total_num_iterations

    @property
    def _head_position(self) -> Vector2D:
        return self._head_to_tail[0]

    def update_rope(self, rope: Rope) -> None:
        self._head_to_tail = list(rope.positions_head_to_tail())
        self._visited_by_tail.add(rope.tail_position)
        new_center_x = min(
            max(self._center.x, self._head_position.x - self._focus_length),
            self._head_position.x + self._focus_length,
        )
        new_center_y = min(
            max(self._center.y, self._head_position.y - self._focus_length),
            self._head_position.y + self._focus_length,
        )
        self._center = Vector2D(new_center_x, new_center_y)

    @staticmethod
    def _is_landscape_marker(pos: Vector2D) -> bool:
        return (pos.x + pos.y * pos.y) % 31 == (pos.x * pos.y) % 19

    def frame(self) -> str:
        x_start = self._center.x - self._width // 2
        y_start = self._center.y - self._height // 2
        frame = ""
        for y in range(y_start, y_start + self._height):
            for x in range(x_start, x_start + self._width):
                pos = Vector2D(x, y)
                if pos == self._head_position:
                    frame += "X"
                elif pos in self._head_to_tail:
                    frame += "O"
                elif self._is_landscape_marker(pos):
                    frame += "*"
                else:
                    frame += "."
            frame += "\n"
        self._iteration += 1
        frame += (
            f"Iteration: {self._iteration}/{self._total_num_iterations} / "
            f"Visited by tail: {len(self._visited_by_tail)}"
        )
        return frame
