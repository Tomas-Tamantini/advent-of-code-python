from dataclasses import dataclass

from models.common.vectors import CardinalDirection, TurnDirection, Vector2D


@dataclass(frozen=True)
class BoardPiece:
    position: Vector2D
    facing: CardinalDirection

    def step_forward(self) -> "BoardPiece":
        return BoardPiece(
            self.position.move(self.facing, y_grows_down=True), self.facing
        )

    def turn(self, turn_direction: TurnDirection) -> "BoardPiece":
        return BoardPiece(self.position, self.facing.turn(turn_direction))
