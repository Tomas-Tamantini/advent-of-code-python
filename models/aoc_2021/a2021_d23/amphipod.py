from dataclasses import dataclass
from .amphipod_burrow import BurrowPosition


@dataclass(frozen=True)
class Amphipod:
    position: BurrowPosition
    desired_room_index: int
    energy_spent_per_step: int
    num_moves: int = 0

    def energy_to_move(self, new_position: BurrowPosition) -> int:
        return self.energy_spent_per_step * self.position.distance(new_position)


@dataclass(frozen=True)
class AmphipodArrangement:
    amphipods: tuple[Amphipod, ...]

    def energy_to_move(self, other: "AmphipodArrangement") -> int:
        return sum(
            amph_a.energy_to_move(amph_b.position)
            for amph_a, amph_b in zip(self.amphipods, other.amphipods)
        )
