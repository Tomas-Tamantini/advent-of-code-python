from typing import Protocol, Union, Optional
from dataclasses import dataclass
from models.assembly import Processor, Memory, SerialOutput


class Instruction(Protocol):
    def execute(
        self,
        processor: Processor,
        memory: Optional[Memory] = None,
        serial_output: Optional[SerialOutput] = None,
    ) -> None:
        ...


@dataclass(frozen=True)
class CopyInstruction:
    source: Union[chr, int]
    destination: Union[chr, int]

    def execute(self, processor: Processor, *_, **__) -> None:
        if not isinstance(self.destination, int):
            processor.registers[self.destination] = processor.get_value(self.source)
        processor.program_counter += 1


@dataclass(frozen=True)
class IncrementInstruction:
    register: Union[chr, int]

    def execute(self, processor: Processor, *_, **__) -> None:
        if not isinstance(self.register, int):
            processor.registers[self.register] += 1
        processor.program_counter += 1


@dataclass(frozen=True)
class DecrementInstruction:
    register: Union[chr, int]

    def execute(self, processor: Processor, *_, **__) -> None:
        if not isinstance(self.register, int):
            processor.registers[self.register] -= 1
        processor.program_counter += 1


@dataclass(frozen=True)
class JumpNotZeroInstruction:
    value_to_compare: Union[chr, int]
    offset: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value(self.value_to_compare) != 0

    def execute(self, processor: Processor, *_, **__) -> None:
        if self._should_jump(processor):
            processor.program_counter += processor.get_value(self.offset)
        else:
            processor.program_counter += 1


@dataclass(frozen=True)
class AddInstruction:
    source: chr
    destination: chr

    def execute(self, processor: Processor, *_, **__) -> None:
        processor.registers[self.destination] += processor.registers[self.source]
        processor.program_counter += 1


@dataclass(frozen=True)
class AddAndMultiplyInstruction:
    source_1: chr
    source_2: chr
    destination: chr

    def execute(self, processor: Processor, *_, **__) -> None:
        processor.registers[self.destination] += (
            processor.registers[self.source_1] * processor.registers[self.source_2]
        )
        processor.program_counter += 1


@dataclass(frozen=True)
class ToggleInstruction:
    offset: Union[chr, int]

    def execute(self, processor: Processor, memory: Memory, *_, **__) -> None:
        offset_value = processor.get_value(self.offset)
        instruction_idx = processor.program_counter + offset_value
        instruction = memory.get_at(instruction_idx)
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
            memory.update_at(instruction_idx, new_instruction)
        processor.program_counter += 1


@dataclass
class OutInstruction:
    source: chr

    def execute(
        self,
        processor: Processor,
        memory: Optional[Memory] = None,
        serial_output: Optional[SerialOutput] = None,
    ) -> None:
        serial_output.write(processor.get_value(self.source))
        processor.program_counter += 1
