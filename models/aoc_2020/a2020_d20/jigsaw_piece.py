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
    def __init__(self, piece_id: int, image_rows: list[str]) -> None:
        self._piece_id = piece_id
        self._orientation = JigsawPieceOrientation(
            num_quarter_turns=0, is_flipped=False
        )
        self._image = np.array([[c == "#" for c in row] for row in image_rows])

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
    def _center_of_rotation(self) -> tuple[float, float]:
        return ((self.width - 1) / 2, (self.height - 1) / 2)

    def _value_at(self, position: Vector2D) -> bool:
        pos_in_img = self._orientation.original_position(
            new_position=position, center_of_rotation=self._center_of_rotation
        )
        return self._image[pos_in_img.y, pos_in_img.x]

    def render(self) -> str:
        return "\n".join(
            "".join(
                "#" if self._value_at(Vector2D(x, y)) else "."
                for x in range(self.width)
            )
            for y in range(self.height)
        )

    def reorient(self, orientation: JigsawPieceOrientation) -> None:
        self._orientation = orientation

    def _bits_along_edge(self, edge: CardinalDirection) -> Iterator[bool]:
        if edge.is_vertical:
            y_value = 0 if edge == CardinalDirection.NORTH else self.height - 1
            for x in range(self.width):
                yield self._value_at(Vector2D(x, y_value))
        else:
            x_value = 0 if edge == CardinalDirection.WEST else self.width - 1
            for y in range(self.height):
                yield self._value_at(Vector2D(x_value, y))

    def can_place_other(
        self, other: "JigsawPiece", relative_placement: CardinalDirection
    ) -> bool:
        for my_bit, other_bit in zip(
            self._bits_along_edge(relative_placement),
            other._bits_along_edge(relative_placement.reverse()),
        ):
            if my_bit != other_bit:
                return False
        return True

    def __hash__(self) -> int:
        return hash(self._piece_id)

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, JigsawPieceBinaryImage)
            and self._piece_id == value.piece_id
        )
