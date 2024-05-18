from dataclasses import dataclass
from models.common.number_theory import ChineseRemainder, solve_chinese_remainder_system


@dataclass(frozen=True)
class SpinningDisc:
    num_positions: int
    position_at_time_zero: int

    def times_to_press_button(
        self, distance_to_capsule_dropping_mechanism: int
    ) -> ChineseRemainder:
        remainder = -self.position_at_time_zero - distance_to_capsule_dropping_mechanism
        return ChineseRemainder(
            divisor=self.num_positions,
            remainder=remainder % self.num_positions,
        )


class DiscSystem:
    def __init__(self, discs):
        self._discs = discs

    def add_disc(self, disc: SpinningDisc):
        self._discs.append(disc)

    def time_to_press_button(self):
        remainders = [
            disc.times_to_press_button(distance_to_capsule_dropping_mechanism=i + 1)
            for i, disc in enumerate(self._discs)
        ]
        return solve_chinese_remainder_system(*remainders)
