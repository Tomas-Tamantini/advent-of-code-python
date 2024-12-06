from typing import Hashable, Protocol

import numpy as np

from models.common.vectors import CardinalDirection

from .jigsaw_piece_orientation import JigsawPieceOrientation


class JigsawPiece(Protocol):
    @property
    def piece_id(self) -> Hashable: ...

    def reorient(self, orientation: JigsawPieceOrientation) -> "JigsawPiece": ...

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool: ...

    def render_without_border_details(self) -> np.array: ...


class JigsawPieceBinaryImage:
    def __init__(self, piece_id: int, image: np.array) -> None:
        self._piece_id = piece_id
        self._image = image

    @classmethod
    def from_string(
        cls, piece_id: int, image_rows: list[str]
    ) -> "JigsawPieceBinaryImage":
        return cls(piece_id, np.array([[c == "#" for c in row] for row in image_rows]))

    @property
    def piece_id(self) -> Hashable:
        return self._piece_id

    @property
    def width(self) -> int:
        return self._image.shape[1]

    @property
    def height(self) -> int:
        return self._image.shape[0]

    def render(self) -> str:
        return "\n".join(
            "".join("#" if cell else "." for cell in row) for row in self._image
        )

    def reorient(self, orientation: JigsawPieceOrientation) -> "JigsawPieceBinaryImage":
        new_image = orientation.transform(self._image)
        return JigsawPieceBinaryImage(self._piece_id, new_image)

    def _bits_along_edge(self, edge: CardinalDirection) -> np.array:
        if edge.is_vertical:
            y_value = 0 if edge == CardinalDirection.NORTH else self.height - 1
            return self._image[y_value, :]
        else:
            x_value = 0 if edge == CardinalDirection.WEST else self.width - 1
            return self._image[:, x_value]

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool:
        self_edge = self._bits_along_edge(relative_placement)
        other_edge = other._bits_along_edge(relative_placement.reverse())
        return np.array_equal(self_edge, other_edge)

    def render_without_border_details(self) -> np.array:
        return self._image[1:-1, 1:-1]
