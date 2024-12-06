from dataclasses import dataclass

from .amphipod import Amphipod


@dataclass(frozen=True)
class AmphipodRoom:
    index: int
    capacity: int
    position_in_hallway: int
    amphipods_back_to_front: tuple[Amphipod, ...]

    @property
    def num_steps_to_enter(self) -> int:
        return self.capacity - len(self.amphipods_back_to_front)

    @property
    def num_steps_to_leave(self) -> int:
        return self.num_steps_to_enter + 1

    def horizontal_distance(self, position: int) -> int:
        return abs(self.position_in_hallway - position)

    def can_pop(self) -> bool:
        return any(
            amphipod.desired_room_index != self.index
            for amphipod in self.amphipods_back_to_front
        )

    def can_push(self) -> bool:
        return len(self.amphipods_back_to_front) < self.capacity and all(
            amphipod.desired_room_index == self.index
            for amphipod in self.amphipods_back_to_front
        )

    def peek(self) -> Amphipod:
        return self.amphipods_back_to_front[-1]

    def pop(self) -> "AmphipodRoom":
        return AmphipodRoom(
            index=self.index,
            capacity=self.capacity,
            position_in_hallway=self.position_in_hallway,
            amphipods_back_to_front=self.amphipods_back_to_front[:-1],
        )

    def push(self, amphipod: Amphipod) -> "AmphipodRoom":
        return AmphipodRoom(
            index=self.index,
            capacity=self.capacity,
            position_in_hallway=self.position_in_hallway,
            amphipods_back_to_front=self.amphipods_back_to_front + (amphipod,),
        )

    def filled(self, energy_per_step: int) -> "AmphipodRoom":
        amphipods = tuple(
            Amphipod(
                desired_room_index=self.index,
                energy_spent_per_step=energy_per_step,
            )
            for _ in range(self.capacity)
        )
        return AmphipodRoom(
            index=self.index,
            capacity=self.capacity,
            position_in_hallway=self.position_in_hallway,
            amphipods_back_to_front=amphipods,
        )
