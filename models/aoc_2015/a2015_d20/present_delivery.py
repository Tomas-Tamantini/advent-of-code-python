from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class _PresentDeliveringElf:
    assigned_number: int
    presents_per_house: int
    houses_to_visit: Optional[int] = None

    def deliver_presents_and_returns_first_house_to_hit_target(
        self, houses: list[int], target_number_of_presents: int
    ) -> Optional[int]:
        houses_count = 0
        for i in range(self.assigned_number, len(houses), self.assigned_number):
            houses_count += 1
            if self.houses_to_visit and houses_count > self.houses_to_visit:
                break
            houses[i] += self.presents_per_house
            if houses[i] >= target_number_of_presents:
                return i


def first_house_to_receive_n_presents(
    target_num_presents: int,
    presents_multiple_per_elf: int,
    houses_per_elf: Optional[int] = None,
) -> int:
    house_idx_limit = min(1_000_000, target_num_presents)
    min_house_idx = house_idx_limit + 1
    presents_received = [0] * (house_idx_limit + 1)
    for i in range(1, house_idx_limit + 1):
        if i >= min_house_idx:
            return min_house_idx
        elf = _PresentDeliveringElf(i, presents_multiple_per_elf * i, houses_per_elf)
        house_to_hit_target = (
            elf.deliver_presents_and_returns_first_house_to_hit_target(
                presents_received, target_num_presents
            )
        )
        if house_to_hit_target and house_to_hit_target < min_house_idx:
            min_house_idx = house_to_hit_target
    if min_house_idx > house_idx_limit:
        raise ValueError(f"House index exceeds {house_idx_limit}")
    return min_house_idx
