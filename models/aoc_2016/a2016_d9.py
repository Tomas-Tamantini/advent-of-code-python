import re
from typing import Iterator


class TextDecompressor:
    def __init__(self, compressed_text: str) -> None:
        self._compressed_text = compressed_text

    def _markers_start_end(self) -> Iterator[tuple[int, int]]:
        for match in re.finditer(r"\((\d+)x(\d+)\)", self._compressed_text):
            yield (match.start(), match.end())

    def _parse_marker(self, marker: str) -> tuple[int, int]:
        return tuple(int(value) for value in marker[1:-1].split("x"))

    def length_decompressed(self) -> int:
        previous_marker_end = -1
        length = len(self._compressed_text)
        for start, end in self._markers_start_end():
            if start < previous_marker_end:
                continue
            length -= end - start
            num_chars, multiplier = self._parse_marker(self._compressed_text[start:end])
            previous_marker_end = end + num_chars
            num_chars_ahead = min(num_chars, len(self._compressed_text) - end)
            length += (multiplier - 1) * num_chars_ahead
        return length
