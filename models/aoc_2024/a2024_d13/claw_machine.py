from dataclasses import dataclass

from models.common.vectors import Vector2D, solve_linear_system_exactly


@dataclass(frozen=True)
class ClawMachine:
    btn_a_offset: Vector2D
    btn_b_offset: Vector2D
    prize_location: Vector2D

    def num_button_presses_to_get_prize(self) -> tuple[int, int]:
        matrix = [
            [self.btn_a_offset.x, self.btn_b_offset.x],
            [self.btn_a_offset.y, self.btn_b_offset.y],
        ]
        prize = [self.prize_location.x, self.prize_location.y]
        solution = solve_linear_system_exactly(matrix, prize)
        if any(sol.denominator != 1 for sol in solution) or any(
            sol.numerator > 100 for sol in solution
        ):
            return None
        else:
            return tuple(sol.numerator for sol in solution)
