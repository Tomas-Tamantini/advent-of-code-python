# TODO: Refactor tests and implementation

from typing import Iterator, Optional
from dataclasses import dataclass
from enum import Enum


class RoomPositioning(int, Enum):
    HALLWAY = 0
    FRONT_OF_ROOM = 1
    BACK_OF_ROOM = 2


@dataclass(frozen=True)
class BurrowPosition:
    position_in_hallway: int
    room_positioning: RoomPositioning

    def distance(self, other: "BurrowPosition") -> int:
        if self.position_in_hallway == other.position_in_hallway:
            return abs(self.room_positioning - other.room_positioning)
        else:
            return (
                abs(self.position_in_hallway - other.position_in_hallway)
                + self.room_positioning
                + other.room_positioning
            )


@dataclass(frozen=True)
class AmphipodBurrow:
    hallway_length: int
    room_positions_in_hallway: tuple[int, ...]

    def reachable_room_position(
        self,
        amphipod,
        other_amphipods: set,
    ) -> Optional[BurrowPosition]:
        occupied_positions = {amphipod.position for amphipod in other_amphipods}
        min_i, max_i = self._reachable_range(amphipod.position, occupied_positions)
        room_position = self.room_positions_in_hallway[amphipod.desired_room_index]
        front_position = BurrowPosition(
            position_in_hallway=room_position,
            room_positioning=RoomPositioning.FRONT_OF_ROOM,
        )
        if (
            room_position < min_i
            or room_position > max_i
            or (front_position in occupied_positions)
        ):
            return None
        back_position = BurrowPosition(
            position_in_hallway=room_position,
            room_positioning=RoomPositioning.BACK_OF_ROOM,
        )
        amphipod_in_back_of_room = None
        for other_amphipod in other_amphipods:
            if other_amphipod.position == back_position:
                amphipod_in_back_of_room = other_amphipod
                break
        if amphipod_in_back_of_room is None:
            return back_position
        elif amphipod_in_back_of_room.desired_room_index == amphipod.desired_room_index:
            return front_position

    def reachable_hallway_positions(
        self, current_position: BurrowPosition, occupied_positions: set[BurrowPosition]
    ) -> Iterator[BurrowPosition]:
        if self._is_blocked_by_amphipod_in_front(current_position, occupied_positions):
            return
        min_i, max_i = self._reachable_range(current_position, occupied_positions)
        for i in range(min_i, max_i + 1):
            if i not in self.room_positions_in_hallway:
                yield BurrowPosition(
                    position_in_hallway=i, room_positioning=RoomPositioning.HALLWAY
                )

    def is_in_proper_room(self, amphipod) -> bool:
        return amphipod.position.room_positioning != RoomPositioning.HALLWAY and (
            amphipod.position.position_in_hallway
            == self.room_positions_in_hallway[amphipod.desired_room_index]
        )

    def _reachable_range(
        self, current_position: BurrowPosition, occupied_positions: set[BurrowPosition]
    ) -> tuple[int, int]:
        occupied_hallway_indices = {
            p.position_in_hallway
            for p in occupied_positions
            if p.room_positioning == RoomPositioning.HALLWAY and p != current_position
        }
        min_range = max(
            (
                i + 1
                for i in occupied_hallway_indices
                if i <= current_position.position_in_hallway
            ),
            default=0,
        )
        max_range = min(
            (
                i - 1
                for i in occupied_hallway_indices
                if i >= current_position.position_in_hallway
            ),
            default=self.hallway_length - 1,
        )
        return min_range, max_range

    def _is_blocked_by_amphipod_in_front(
        self, current_position: BurrowPosition, occupied_positions: set[BurrowPosition]
    ):
        return current_position.room_positioning == RoomPositioning.BACK_OF_ROOM and (
            BurrowPosition(
                position_in_hallway=current_position.position_in_hallway,
                room_positioning=RoomPositioning.FRONT_OF_ROOM,
            )
            in occupied_positions
        )
