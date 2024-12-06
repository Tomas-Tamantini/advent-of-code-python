from typing import Iterator, Optional

from models.common.assembly import Instruction

from .instruction_parser import parse_next_instruction


class IntcodeProgram:
    def __init__(self, instructions: list[int]) -> None:
        self._instructions = {
            address: value for address, value in enumerate(instructions)
        }

    @property
    def contiguous_instructions(self) -> Iterator[int]:
        idx = 0
        while idx in self._instructions:
            yield self._instructions[idx]
            idx += 1

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        if program_counter < 0:
            return None
        param_list = [self.read(program_counter + i) for i in range(4)]
        return parse_next_instruction(param_list)

    def read(self, address: int) -> int:
        if address < 0:
            raise IndexError("Address must be non-negative")
        return self._instructions.get(address, 0)

    def write(self, address: int, new_value) -> None:
        if address < 0:
            raise IndexError("Address must be non-negative")
        self._instructions[address] = new_value
