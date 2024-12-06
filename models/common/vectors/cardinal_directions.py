from enum import Enum
from typing import Iterator


class TurnDirection(Enum):
    LEFT = "L"
    RIGHT = "R"
    NO_TURN = "N"
    U_TURN = "U"


class CardinalDirection(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def is_vertical(self) -> bool:
        return self in {CardinalDirection.NORTH, CardinalDirection.SOUTH}

    @property
    def is_horizontal(self) -> bool:
        return self in {CardinalDirection.EAST, CardinalDirection.WEST}

    def turn(self, turn_direction: TurnDirection) -> "CardinalDirection":
        if turn_direction == TurnDirection.LEFT:
            return self.turn_left()
        elif turn_direction == TurnDirection.RIGHT:
            return self.turn_right()
        elif turn_direction == TurnDirection.U_TURN:
            return self.reverse()
        else:
            return self

    def turn_left(self) -> "CardinalDirection":
        return CardinalDirection((self.value - 1) % 4)

    def turn_right(self) -> "CardinalDirection":
        return CardinalDirection((self.value + 1) % 4)

    def reverse(self) -> "CardinalDirection":
        return CardinalDirection((self.value + 2) % 4)

    def offset(self) -> tuple[int, int]:
        if self == CardinalDirection.NORTH:
            return 0, 1
        elif self == CardinalDirection.EAST:
            return 1, 0
        elif self == CardinalDirection.SOUTH:
            return 0, -1
        else:
            return -1, 0

    @staticmethod
    def reading_order() -> Iterator["CardinalDirection"]:
        yield CardinalDirection.NORTH
        yield CardinalDirection.WEST
        yield CardinalDirection.EAST
        yield CardinalDirection.SOUTH
