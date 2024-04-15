from typing import Optional, Iterator
from models.assembly import Instruction
from .game_console_instructions import JumpOrNoOpInstruction


class GameConsoleProgram:
    def __init__(
        self, instructions: list[Instruction], index_to_toggle: int = -1
    ) -> None:
        self._instructions = instructions
        self._executed = set()
        self._index_to_toggle = index_to_toggle
        if index_to_toggle >= 0 and not isinstance(
            instructions[index_to_toggle], JumpOrNoOpInstruction
        ):
            raise IndexError("Index to toggle must be a JumpOrNoOpInstruction.")

    @staticmethod
    def indices_which_can_be_toggled(instructions: list[Instruction]) -> Iterator[int]:
        for i, instruction in enumerate(instructions):
            if isinstance(instruction, JumpOrNoOpInstruction):
                yield i

    def get_instruction(self, program_counter: int) -> Optional[Instruction]:
        if program_counter < 0 or program_counter >= len(self._instructions):
            return None
        if program_counter in self._executed:
            raise self.RepeatedInstructionError()
        self._executed.add(program_counter)
        if program_counter == self._index_to_toggle:
            return self._instructions[program_counter].toggle()
        else:
            return self._instructions[program_counter]

    class RepeatedInstructionError(Exception):
        pass
