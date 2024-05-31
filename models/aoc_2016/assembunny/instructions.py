from typing import Union
from dataclasses import dataclass
from models.common.assembly import Hardware, CopyInstruction, JumpNotZeroInstruction


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
        offset_value = hardware.processor.get_value_or_immediate(self.offset)
        instruction_idx = hardware.processor.program_counter + offset_value
        instruction = hardware.memory.read(instruction_idx)
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
                value_to_compare=instruction.source,
                offset=instruction.destination,
            )
        if new_instruction:
            hardware.memory.write(instruction_idx, new_instruction)
        hardware.increment_program_counter()
