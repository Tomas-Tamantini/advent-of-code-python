from dataclasses import dataclass
from typing import Protocol
from models.vectors import Vector2D, CardinalDirection, TurnDirection


@dataclass(frozen=True)
class Ship:
    position: Vector2D
    facing: CardinalDirection


class NavigationInstruction(Protocol):
    def execute(self, ship: Ship) -> Ship: ...


@dataclass(frozen=True)
class MoveShipInstruction:
    direction: CardinalDirection
    distance: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position.move(self.direction, self.distance),
            facing=ship.facing,
        )


@dataclass(frozen=True)
class MoveShipForwardInstruction:
    distance: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position.move(ship.facing, self.distance), facing=ship.facing
        )


@dataclass(frozen=True)
class TurnShipInstruction:
    turn_direction: TurnDirection

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position, facing=ship.facing.turn(self.turn_direction)
        )
