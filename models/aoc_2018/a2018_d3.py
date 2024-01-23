from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class FabricRectangle:
    id: int
    inches_from_left: int
    inches_from_top: int
    width: int
    height: int

    @property
    def end_inches_from_left(self) -> int:
        return self.inches_from_left + self.width

    @property
    def end_inches_from_top(self) -> int:
        return self.inches_from_top + self.height

    def intersection(self, other: "FabricRectangle") -> Iterator[tuple[int, int]]:
        x_start = max(self.inches_from_left, other.inches_from_left)
        x_end = min(self.end_inches_from_left, other.end_inches_from_left)
        y_start = max(self.inches_from_top, other.inches_from_top)
        y_end = min(self.end_inches_from_top, other.end_inches_from_top)
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                yield x, y


class FabricArea:
    def __init__(self) -> None:
        self._points_with_more_than_one_claim = set()

    def distribute(self, rectangles: list[FabricRectangle]) -> None:
        sorted_rectangles = sorted(
            rectangles, key=lambda rectangle: rectangle.inches_from_top
        )
        for i, rectangle_a in enumerate(sorted_rectangles):
            for rectangle_b in sorted_rectangles[i + 1 :]:
                if rectangle_a.end_inches_from_top < rectangle_b.inches_from_top:
                    break
                self._points_with_more_than_one_claim.update(
                    set(rectangle_a.intersection(rectangle_b))
                )

    @property
    def points_with_more_than_one_claim(self) -> set[tuple[int, int]]:
        return self._points_with_more_than_one_claim
