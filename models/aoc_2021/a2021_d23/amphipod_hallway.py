from dataclasses import dataclass
from typing import Optional, Iterator
from .amphipod import Amphipod
from .amphipod_room import AmphipodRoom


@dataclass(frozen=True)
class AmphipodHallway:
    positions: tuple[Optional[Amphipod], ...]

    def _reachable_range_from(self, position: int) -> tuple[int, int]:
        min_range, max_range = 0, len(self.positions) - 1
        for i in range(position, -1, -1):
            if self.positions[i] is not None:
                min_range = i + 1
                break
        for i in range(position, len(self.positions)):
            if self.positions[i] is not None:
                max_range = i - 1
                break
        return min_range, max_range

    def positions_reachable_from(
        self, position: int, room_positions: set[int]
    ) -> Iterator[int]:
        min_range, max_range = self._reachable_range_from(position)
        for i in range(min_range, max_range + 1):
            if i not in room_positions:
                yield i

    def insert_at(self, position: int, amphipod: Amphipod) -> "AmphipodHallway":
        new_positions = list(self.positions)
        new_positions[position] = amphipod
        return AmphipodHallway(tuple(new_positions))

    def remove_at(self, position: int) -> "AmphipodHallway":
        new_positions = list(self.positions)
        new_positions[position] = None
        return AmphipodHallway(tuple(new_positions))

    def amphipods_that_can_move_to_room(
        self, room: AmphipodRoom
    ) -> Iterator[tuple[int, Amphipod]]:
        for i in range(room.position_in_hallway, -1, -1):
            if self.positions[i] is not None:
                if self.positions[i].desired_room_index == room.index:
                    yield i, self.positions[i]
                break

        for i in range(room.position_in_hallway, len(self.positions)):
            if self.positions[i] is not None:
                if self.positions[i].desired_room_index == room.index:
                    yield i, self.positions[i]
                break

    def emptied(self) -> "AmphipodHallway":
        return AmphipodHallway(tuple([None for _ in self.positions]))

    def all_amphipods(self) -> Iterator[Amphipod]:
        for position in self.positions:
            if position is not None:
                yield position
