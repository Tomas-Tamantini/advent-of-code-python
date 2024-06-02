from models.common.vectors import CardinalDirection
from dataclasses import dataclass


@dataclass(frozen=True)
class MoveCommand:
    direction: CardinalDirection

    def __str__(self) -> str:
        return {
            CardinalDirection.NORTH: "north",
            CardinalDirection.EAST: "east",
            CardinalDirection.SOUTH: "south",
            CardinalDirection.WEST: "west",
        }[self.direction]


@dataclass(frozen=True)
class TakeCommand:
    item: str

    def __str__(self) -> str:
        return f"take {self.item}"


@dataclass(frozen=True)
class DropCommand:
    item: str

    def __str__(self) -> str:
        return f"drop {self.item}"


class InventoryCommand:
    def __str__(self) -> str:
        return "inv"
