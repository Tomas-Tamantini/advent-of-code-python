from dataclasses import dataclass
from typing import Optional, Iterator
from .amphipod import Amphipod
from .amphipod_room import AmphipodRoom


@dataclass(frozen=True)
class AmphipodHallway:
    positions: tuple[Optional[Amphipod], ...]

    def _rightmost_occupied_position_to_the_left(self, position: int) -> Optional[int]:
        for i in range(position, -1, -1):
            if self.positions[i] is not None:
                return i

    def _leftmost_occupied_position_to_the_right(self, position: int) -> Optional[int]:
        for i in range(position, len(self.positions)):
            if self.positions[i] is not None:
                return i

    def _reachable_range_from(self, position: int) -> tuple[int, int]:
        rightmost_to_left = self._rightmost_occupied_position_to_the_left(position)
        min_range = rightmost_to_left + 1 if rightmost_to_left is not None else 0
        leftmost_to_right = self._leftmost_occupied_position_to_the_right(position)
        max_range = (
            leftmost_to_right - 1
            if leftmost_to_right is not None
            else len(self.positions) - 1
        )
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
        candidate_positions = (
            self._rightmost_occupied_position_to_the_left(room.position_in_hallway),
            self._leftmost_occupied_position_to_the_right(room.position_in_hallway),
        )
        for i in candidate_positions:
            if i is not None and self.positions[i].desired_room_index == room.index:
                yield i, self.positions[i]

    def emptied(self) -> "AmphipodHallway":
        return AmphipodHallway(tuple([None for _ in self.positions]))

    def all_amphipods(self) -> Iterator[Amphipod]:
        for position in self.positions:
            if position is not None:
                yield position
