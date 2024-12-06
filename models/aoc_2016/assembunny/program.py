from models.common.assembly import (
    AddInstruction,
    CopyInstruction,
    Instruction,
    JumpNotZeroInstruction,
    MutableProgram,
)

from .instructions import (
    AddAndMultiplyInstruction,
    DecrementInstruction,
    IncrementInstruction,
)


class AssembunnyProgram(MutableProgram):
    def read(self, index: int) -> int:
        return self.get_instruction(index)

    def write(self, index: int, new_value: Instruction) -> None:
        return self.update_instruction(index, new_value)

    def optimize(self) -> None:
        # These optimizations are specific to the programs given
        # In a more general case, they will introduce bugs
        for index in range(len(self._instructions)):
            instruction = self._instructions[index]
            if isinstance(instruction, JumpNotZeroInstruction):
                if instruction.offset == -2 and index >= 2:
                    instruction_1 = self._instructions[index - 2]
                    instruction_2 = self._instructions[index - 1]
                    if (
                        isinstance(instruction_1, IncrementInstruction)
                        and isinstance(instruction_2, DecrementInstruction)
                        and instruction_2.register == instruction.value_to_compare
                    ):
                        self._instructions[index - 2] = AddInstruction(
                            instruction.value_to_compare,
                            instruction_1.register,
                        )
                        self._instructions[index - 1] = CopyInstruction(
                            0, instruction.value_to_compare
                        )

                elif instruction.offset == -5 and index >= 5:
                    instruction_1 = self._instructions[index - 5]
                    instruction_2 = self._instructions[index - 4]
                    instruction_3 = self._instructions[index - 3]
                    instruction_4 = self._instructions[index - 2]
                    instruction_5 = self._instructions[index - 1]

                    if (
                        isinstance(instruction_1, CopyInstruction)
                        and isinstance(instruction_2, AddInstruction)
                        and isinstance(instruction_3, CopyInstruction)
                        and isinstance(instruction_4, JumpNotZeroInstruction)
                        and isinstance(instruction_5, DecrementInstruction)
                        and instruction_1.destination
                        == instruction_2.source
                        == instruction_3.destination
                        == instruction_4.value_to_compare
                        and instruction_5.register == instruction.value_to_compare
                    ):
                        self._instructions[index - 4] = AddAndMultiplyInstruction(
                            source_1=instruction_1.destination,
                            source_2=instruction.value_to_compare,
                            destination=instruction_2.destination,
                        )
                        self._instructions[index - 1] = CopyInstruction(
                            0, instruction.value_to_compare
                        )
