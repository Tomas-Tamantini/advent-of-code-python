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
        self, new_position: Vector2D, center_of_rotation: tuple[float, float]
    ) -> Vector2D:
        dx = new_position.x - center_of_rotation[0]
        dy = new_position.y - center_of_rotation[1]
        for _ in range(self.num_quarter_turns):
            dx, dy = dy, -dx
        if self.is_flipped:
            dx = -dx
        new_x = center_of_rotation[0] + dx
        new_y = center_of_rotation[1] + dy
        return Vector2D(round(new_x), round(new_y))
