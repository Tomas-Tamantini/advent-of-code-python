from dataclasses import dataclass

from models.common.vectors import Vector2D, solve_linear_system_exactly


@dataclass(frozen=True)
class ClawMachine:
    btn_a_offset: Vector2D
    btn_b_offset: Vector2D
    prize_location: Vector2D

    def offset_prize(self, offset: int) -> "ClawMachine":
        return ClawMachine(
            btn_a_offset=self.btn_a_offset,
            btn_b_offset=self.btn_b_offset,
            prize_location=self.prize_location + Vector2D(offset, offset),
        )

    def num_button_presses_to_get_prize(self) -> tuple[int, int]:
        matrix = [
            [self.btn_a_offset.x, self.btn_b_offset.x],
            [self.btn_a_offset.y, self.btn_b_offset.y],
        ]
        prize = [self.prize_location.x, self.prize_location.y]
        solution = solve_linear_system_exactly(matrix, prize)
        if any(sol.denominator != 1 for sol in solution):
            return None
        else:
            return tuple(sol.numerator for sol in solution)
