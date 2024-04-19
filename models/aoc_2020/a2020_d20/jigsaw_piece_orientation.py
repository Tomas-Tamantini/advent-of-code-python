from dataclasses import dataclass
from models.vectors import Vector2D


@dataclass(frozen=True)
class JigsawPieceOrientation:
    num_quarter_turns: int
    is_flipped: bool

    @staticmethod
    def all_possible_orientations():
        for num_quarter_turns in range(4):
            for is_flipped in (False, True):
                yield JigsawPieceOrientation(num_quarter_turns, is_flipped)

    def original_position(
        self, new_position: Vector2D, center_of_rotation: Vector2D
    ) -> Vector2D:
        diff = new_position - center_of_rotation
        dx, dy = diff.x, diff.y
        for _ in range(self.num_quarter_turns):
            dx, dy = dy, -dx
        if self.is_flipped:
            dx = -dx
        return center_of_rotation + Vector2D(dx, dy)
