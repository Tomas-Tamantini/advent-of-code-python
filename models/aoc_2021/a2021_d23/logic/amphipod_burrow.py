from dataclasses import dataclass
from typing import Iterator

from .amphipod import Amphipod
from .amphipod_hallway import AmphipodHallway
from .amphipod_room import AmphipodRoom


@dataclass(frozen=True)
class AmphipodBurrow:
    hallway: AmphipodHallway
    rooms: tuple[AmphipodRoom, ...]

    def _all_amphipods(self) -> Iterator[Amphipod]:
        yield from self.hallway.all_amphipods()
        for room in self.rooms:
            yield from room.amphipods_back_to_front

    def terminal_state(self) -> "AmphipodBurrow":
        new_hallway = self.hallway.emptied()
        energy_per_step = {
            amphipod.desired_room_index: amphipod.energy_spent_per_step
            for amphipod in self._all_amphipods()
        }
        new_rooms = tuple(
            room.filled(energy_per_step.get(room.index, 0)) for room in self.rooms
        )
        return AmphipodBurrow(new_hallway, new_rooms)

    def _update_burrow(
        self,
        new_hallway: AmphipodHallway,
        new_room: AmphipodRoom,
        room_index_in_tuple: int,
    ) -> "AmphipodBurrow":
        new_rooms = (
            self.rooms[:room_index_in_tuple]
            + (new_room,)
            + self.rooms[room_index_in_tuple + 1 :]
        )
        return AmphipodBurrow(new_hallway, new_rooms)

    def weighted_neighbors(self) -> Iterator[tuple["AmphipodBurrow", int]]:
        room_positions = {room.position_in_hallway for room in self.rooms}
        for i, room in enumerate(self.rooms):
            if room.can_pop():
                for position in self.hallway.positions_reachable_from(
                    room.position_in_hallway, room_positions
                ):
                    amphipod = room.peek()
                    num_steps = room.num_steps_to_leave + room.horizontal_distance(
                        position
                    )
                    energy = num_steps * amphipod.energy_spent_per_step
                    new_room = room.pop()
                    new_hallway = self.hallway.insert_at(position, amphipod)
                    new_burrow = self._update_burrow(new_hallway, new_room, i)
                    yield new_burrow, energy
            elif room.can_push():
                for (
                    hallway_position,
                    amphipod,
                ) in self.hallway.amphipods_that_can_move_to_room(room):
                    num_steps = room.num_steps_to_enter + room.horizontal_distance(
                        hallway_position
                    )
                    energy = num_steps * amphipod.energy_spent_per_step
                    new_room = room.push(amphipod)
                    new_hallway = self.hallway.remove_at(hallway_position)
                    new_burrow = self._update_burrow(new_hallway, new_room, i)
                    yield new_burrow, energy
