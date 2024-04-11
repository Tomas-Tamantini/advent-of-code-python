from typing import Iterator
from .springscript_instruction import SpringScriptInstruction


class SpringDroidInput:
    def __init__(self, instructions: list[SpringScriptInstruction]) -> None:
        self._instructions = instructions
        self._generator = self._char_generator()

    def _char_generator(self) -> Iterator[chr]:
        for instruction in self._instructions:
            yield from str(instruction)
            yield "\n"
        for c in "WALK":
            yield c
        yield "\n"

    def read(self) -> int:
        try:
            return ord(next(self._generator))
        except StopIteration:
            raise self.EmptyBufferError()

    class EmptyBufferError(Exception):
        pass


class SpringDroidOutput:
    def __init__(self) -> None:
        self._ascii_values = []
        self._large_output = None

    def large_output(self) -> int:
        if self._large_output is None:
            raise ValueError("No large output value stored")
        else:
            return self._large_output

    def write(self, value: int) -> None:
        if 0 <= value <= 255:
            self._ascii_values.append(value)
        else:
            self._large_output = value

    def render(self) -> str:
        return "".join(chr(value) for value in self._ascii_values)
