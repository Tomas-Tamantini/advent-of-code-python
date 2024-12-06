from typing import Iterator


class InputFromTextFile:
    def __init__(self, file_name: str):
        self._file_name = file_name

    def read(self) -> str:
        with open(self._file_name, "r", encoding="utf-8") as f:
            return f.read()

    def readlines(self) -> Iterator[str]:
        with open(self._file_name, "r", encoding="utf-8") as f:
            yield from f.readlines()

    def read_stripped_lines(self, keep_empty_lines: bool = False) -> Iterator[str]:
        for line in self.readlines():
            if line.strip() or keep_empty_lines:
                yield line.strip()
