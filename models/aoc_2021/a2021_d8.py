from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class ShuffledSevenDigitDisplay:
    unique_patterns: tuple[str]
    four_digit_output: tuple[str]

    def _patterns_with_n_segments(self, num_segments: int) -> Iterator[set[str]]:
        for pattern in self.unique_patterns:
            if len(pattern) == num_segments:
                yield set(pattern)

    def _digit_to_segments(self) -> dict[int, set[str]]:
        knowns = {
            1: next(self._patterns_with_n_segments(2)),
            4: next(self._patterns_with_n_segments(4)),
            7: next(self._patterns_with_n_segments(3)),
            8: next(self._patterns_with_n_segments(7)),
        }

        for pattern in self._patterns_with_n_segments(6):
            if knowns[4].union(knowns[7]).issubset(pattern):
                knowns[9] = pattern
            elif (knowns[8] - knowns[7]).issubset(pattern):
                knowns[6] = pattern
            else:
                knowns[0] = pattern

        for pattern in self._patterns_with_n_segments(5):
            if pattern.issubset(knowns[6]):
                knowns[5] = pattern
            elif set(pattern).issubset(knowns[9]):
                knowns[3] = pattern
            else:
                knowns[2] = pattern
        return knowns

    def _segments_to_digit(
        self, segments: set[str], mapping: dict[int, set[str]]
    ) -> int:
        for digit, pattern in mapping.items():
            if pattern == segments:
                return digit
        raise ValueError("No digit found for segments")

    def decode(self) -> str:
        knowns = self._digit_to_segments()
        return "".join(
            str(self._segments_to_digit(set(segments), knowns))
            for segments in self.four_digit_output
        )
