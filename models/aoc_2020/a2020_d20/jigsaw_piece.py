from typing import Protocol, Hashable, Iterator
import numpy as np
from models.vectors import CardinalDirection, Vector2D
from .jigsaw_piece_orientation import JigsawPieceOrientation


class JigsawPiece(Protocol):
    @property
    def piece_id(self) -> Hashable: ...

    def reorient(self, orientation: JigsawPieceOrientation) -> None: ...

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool: ...

    def __hash__(self) -> int: ...


class JigsawPieceBinaryImage:
    def __init__(self, piece_id: int, image: list[str]) -> None:
        self._piece_id = piece_id
        self._orientation = JigsawPieceOrientation(
            num_quarter_turns=0, is_flipped=False
        )
        self._image = np.array([[c == "#" for c in row] for row in image])

    @property
    def piece_id(self) -> Hashable:
        return self._piece_id

    @property
    def width(self) -> int:
        return self._image.shape[1]

    @property
    def height(self) -> int:
        return self._image.shape[0]

    @property
    def _center_of_rotation(self) -> Vector2D:
        return Vector2D(self.width // 2, self.height // 2)

    def render(self) -> str:
        rendered = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                p = self._orientation.original_position(
                    new_position=Vector2D(x, y),
                    center_of_rotation=self._center_of_rotation,
                )
                row += "#" if self._image[p.y, p.x] else "."
            rendered.append(row)

        return "\n".join(rendered)

    def reorient(self, orientation: JigsawPieceOrientation) -> None:
        self._orientation = orientation

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool:
        raise NotImplementedError()

    def __hash__(self) -> int:
        return hash(self._piece_id)

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, JigsawPieceBinaryImage)
            and self._piece_id == value.piece_id
        )
