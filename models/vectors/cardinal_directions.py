from enum import Enum


class CardinalDirection(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

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
