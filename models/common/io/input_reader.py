from typing import Iterator, Protocol


class InputReader(Protocol):
    def read(self) -> str: ...

    def readlines(self) -> Iterator[str]: ...

    def read_stripped_lines(self, keep_empty_lines: bool) -> Iterator[str]: ...


class InputFromString:
    def __init__(self, input_content: str) -> None:
        self._content = input_content

    def read(self) -> str:
        return self._content

    def readlines(self) -> Iterator[str]:
        yield from self._content.split("\n")

    def read_stripped_lines(self, keep_empty_lines: bool = False) -> Iterator[str]:
        for line in self.readlines():
            if line.strip() or keep_empty_lines:
                yield line.strip()
