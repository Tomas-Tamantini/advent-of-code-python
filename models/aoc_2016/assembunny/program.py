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
                if self._can_optimize_increment(instruction, index):
                    self._optimize_increment(index, instruction)
                elif self._can_optimize_multi_increment(instruction, index):
                    self._optimize_multi_increment(index, instruction)

    def _optimize_increment(
        self, index: int, instruction: JumpNotZeroInstruction
    ) -> None:
        self._instructions[index - 2] = AddInstruction(
            instruction.value_to_compare,
            self._instructions[index - 2].register,
        )
        self._instructions[index - 1] = CopyInstruction(0, instruction.value_to_compare)

    def _can_optimize_increment(
        self, instruction: JumpNotZeroInstruction, index: int
    ) -> bool:
        if instruction.offset != -2 or index < 2:
            return False
        instruction_1 = self._instructions[index - 2]
        instruction_2 = self._instructions[index - 1]
        return (
            isinstance(instruction_1, IncrementInstruction)
            and isinstance(instruction_2, DecrementInstruction)
            and instruction_2.register == instruction.value_to_compare
        )

    def _optimize_multi_increment(
        self, index: int, instruction: JumpNotZeroInstruction
    ) -> None:
        self._instructions[index - 4] = AddAndMultiplyInstruction(
            source_1=self._instructions[index - 5].destination,
            source_2=instruction.value_to_compare,
            destination=self._instructions[index - 4].destination,
        )
        self._instructions[index - 1] = CopyInstruction(0, instruction.value_to_compare)

    def _can_optimize_multi_increment(
        self, instruction: JumpNotZeroInstruction, index: int
    ) -> bool:
        if instruction.offset != -5 or index < 5:
            return False
        instruction_1 = self._instructions[index - 5]
        instruction_2 = self._instructions[index - 4]
        instruction_3 = self._instructions[index - 3]
        instruction_4 = self._instructions[index - 2]
        instruction_5 = self._instructions[index - 1]

        return (
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
        )
