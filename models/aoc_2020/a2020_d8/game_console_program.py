from models.assembly import Instruction


class GameConsoleProgram:
    def __init__(self, instructions: list[Instruction]) -> None:
        self._instructions = instructions
        self._executed = set()

    def get_instruction(self, program_counter: int) -> Instruction:
        if program_counter < 0 or program_counter >= len(self._instructions):
            raise IndexError
        if program_counter in self._executed:
            raise self.RepeatedInstructionError()
        self._executed.add(program_counter)
        return self._instructions[program_counter]

    class RepeatedInstructionError(Exception):
        pass
