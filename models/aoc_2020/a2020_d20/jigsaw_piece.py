from typing import Protocol, Hashable
from models.vectors import CardinalDirection
from .jigsaw_piece_orientation import JigsawPieceOrientation


class JigsawPiece(Protocol):
    @property
    def piece_id(self) -> Hashable: ...

    def reorient(self, orientation: JigsawPieceOrientation) -> None: ...

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool: ...

    def __hash__(self) -> int: ...
