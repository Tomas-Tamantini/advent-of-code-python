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
