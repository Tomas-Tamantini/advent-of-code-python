from typing import Union
from dataclasses import dataclass
from models.assembly import Instruction, MutableProgram, Processor, Hardware


@dataclass(frozen=True)
class CopyInstruction:
    source: Union[chr, int]
    destination: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if not isinstance(self.destination, int):
            hardware.set_value_at_register(
                self.destination, hardware.processor.get_value(self.source)
            )

        hardware.increment_program_counter()


@dataclass(frozen=True)
class IncrementInstruction:
    register: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if not isinstance(self.register, int):
            hardware.increment_value_at_register(self.register, increment=1)
        hardware.increment_program_counter()


@dataclass(frozen=True)
class DecrementInstruction:
    register: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if not isinstance(self.register, int):
            hardware.increment_value_at_register(self.register, increment=-1)
        hardware.increment_program_counter()


@dataclass(frozen=True)
class JumpNotZeroInstruction:
    value_to_compare: Union[chr, int]
    offset: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value(self.value_to_compare) != 0

    def execute(self, hardware: Hardware) -> None:
        if self._should_jump(hardware.processor):
            hardware.increment_program_counter(
                hardware.processor.get_value(self.offset)
            )
        else:
            hardware.increment_program_counter()


@dataclass(frozen=True)
class AddInstruction:
    source: chr
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.increment_value_at_register(
            self.destination, hardware.processor.get_value(self.source)
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class AddAndMultiplyInstruction:
    source_1: chr
    source_2: chr
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.increment_value_at_register(
            self.destination,
            hardware.get_value_at_register(self.source_1)
            * hardware.get_value_at_register(self.source_2),
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class ToggleInstruction:
    offset: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        offset_value = hardware.processor.get_value(self.offset)
        instruction_idx = hardware.processor.program_counter + offset_value
        instruction = hardware.memory.get_at(instruction_idx)
        new_instruction = None
        if isinstance(instruction, IncrementInstruction):
            new_instruction = DecrementInstruction(instruction.register)
        elif isinstance(instruction, DecrementInstruction):
            new_instruction = IncrementInstruction(instruction.register)
        elif isinstance(instruction, ToggleInstruction):
            new_instruction = IncrementInstruction(instruction.offset)
        elif isinstance(instruction, JumpNotZeroInstruction):
            new_instruction = CopyInstruction(
                instruction.value_to_compare, instruction.offset
            )
        elif isinstance(instruction, CopyInstruction):
            new_instruction = JumpNotZeroInstruction(
                instruction.source, instruction.destination
            )
        if new_instruction:
            hardware.memory.update_at(instruction_idx, new_instruction)
        hardware.increment_program_counter()


@dataclass
class OutInstruction:
    source: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.serial_output.write(hardware.get_value_at_register(self.source))
        hardware.increment_program_counter()


class AssembunnyProgram(MutableProgram):
    def get_at(self, index: int) -> int:
        return self.get_instruction(index)

    def update_at(self, index: int, new_value: Instruction) -> None:
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