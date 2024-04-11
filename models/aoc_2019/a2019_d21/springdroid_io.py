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
