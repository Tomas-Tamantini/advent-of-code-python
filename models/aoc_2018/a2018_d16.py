from dataclasses import dataclass
from typing import Callable, Iterator
from models.assembly import Hardware, Processor


@dataclass(frozen=True)
class RegisterOrImmediate:
    value: int
    is_register: bool

    def get_value(self, hardware: Hardware) -> int:
        if self.is_register:
            return hardware.get_value_at_register(self.value)
        else:
            return self.value


class _ThreeValueInstruction:
    def __init__(
        self,
        register_out: int,
        input_a: RegisterOrImmediate,
        input_b: RegisterOrImmediate,
        operation: Callable[[int, int], int],
    ) -> None:
        self._register_out = register_out
        self._input_a = input_a
        self._input_b = input_b
        self._operation = operation

    def registers_used(self) -> Iterator[int]:
        if self._input_a.is_register:
            yield self._input_a.value
        if self._input_b.is_register:
            yield self._input_b.value
        yield self._register_out

    def execute(self, hardware: Hardware) -> None:
        result = self._operation(
            self._input_a.get_value(hardware),
            self._input_b.get_value(hardware),
        )
        hardware.set_value_at_register(self._register_out, result)


class AddRegisters(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a + b
        super().__init__(register_out, input_a, input_b, operation)


class AddImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a + b
        super().__init__(register_out, input_a, input_b, operation)


class MultiplyRegisters(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a * b
        super().__init__(register_out, input_a, input_b, operation)


class MultiplyImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a * b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseAndRegisters(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a & b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseAndImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a & b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseOrRegisters(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a | b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseOrImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a | b
        super().__init__(register_out, input_a, input_b, operation)


class AssignmentRegisters(_ThreeValueInstruction):
    def __init__(
        self, register_in: int, throwaway_value: int, register_out: int
    ) -> None:
        input_a = RegisterOrImmediate(register_in, is_register=True)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(register_out, input_a, input_b, operation)


class AssignmentImmediate(_ThreeValueInstruction):
    def __init__(self, value_in: int, throwaway_value: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_in, is_register=False)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanImmediateRegister(_ThreeValueInstruction):
    def __init__(self, value_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanRegisterImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanRegisterRegister(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualImmediateRegister(_ThreeValueInstruction):
    def __init__(self, value_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualRegisterImmediate(_ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualRegisterRegister(_ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(register_out, input_a, input_b, operation)


@dataclass(frozen=True)
class InstructionSample:
    op_code: int
    instruction_values: tuple[int, int, int]
    registers_before: tuple[int, ...]
    registers_after: tuple[int, ...]


def _instruction_matches_result(
    instruction: _ThreeValueInstruction,
    instruction_sample: InstructionSample,
) -> bool:
    num_registers = len(instruction_sample.registers_before)
    if any(r < 0 or r >= num_registers for r in instruction.registers_used()):
        return False
    processor = Processor(
        registers=dict(enumerate(instruction_sample.registers_before))
    )
    hardware = Hardware(processor)
    instruction.execute(hardware)
    return processor.registers == dict(enumerate(instruction_sample.registers_after))


ALL_THREE_VALUE_INSTRUCTIONS = [
    AddRegisters,
    AddImmediate,
    MultiplyRegisters,
    MultiplyImmediate,
    BitwiseAndRegisters,
    BitwiseAndImmediate,
    BitwiseOrRegisters,
    BitwiseOrImmediate,
    AssignmentRegisters,
    AssignmentImmediate,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
]


def possible_instructions(
    instruction_sample: InstructionSample,
    candidates: list[type[_ThreeValueInstruction]],
) -> Iterator[type[_ThreeValueInstruction]]:
    for candidate in candidates:
        instruction = candidate(*instruction_sample.instruction_values)
        if _instruction_matches_result(instruction, instruction_sample):
            yield candidate
