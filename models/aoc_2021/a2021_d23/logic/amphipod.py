from dataclasses import dataclass


@dataclass(frozen=True)
class Amphipod:
    desired_room_index: int
    energy_spent_per_step: int
