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
        self._rectangle_without_overlap = None

    def distribute(self, rectangles: list[FabricRectangle]) -> None:
        sorted_rectangles = sorted(
            rectangles, key=lambda rectangle: rectangle.inches_from_top
        )
        overlaps_with_some = [False] * len(rectangles)
        for i in range(len(sorted_rectangles)):
            rectangle_a = sorted_rectangles[i]
            for j in range(i + 1, len(sorted_rectangles)):
                rectangle_b = sorted_rectangles[j]
                if rectangle_a.end_inches_from_top < rectangle_b.inches_from_top:
                    break
                intersection = set(rectangle_a.intersection(rectangle_b))
                if intersection:
                    self._points_with_more_than_one_claim.update(intersection)
                    overlaps_with_some[i] = True
                    overlaps_with_some[j] = True
            if not overlaps_with_some[i]:
                self._rectangle_without_overlap = rectangle_a

    @property
    def points_with_more_than_one_claim(self) -> set[tuple[int, int]]:
        return self._points_with_more_than_one_claim

    @property
    def rectangle_without_overlap(self) -> FabricRectangle:
        return self._rectangle_without_overlap
