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


class ThreeValueInstruction:
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
        hardware.increment_program_counter()


class AddRegisters(ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a + b
        super().__init__(register_out, input_a, input_b, operation)


class AddImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a + b
        super().__init__(register_out, input_a, input_b, operation)


class MultiplyRegisters(ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a * b
        super().__init__(register_out, input_a, input_b, operation)


class MultiplyImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a * b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseAndRegisters(ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a & b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseAndImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a & b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseOrRegisters(ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a | b
        super().__init__(register_out, input_a, input_b, operation)


class BitwiseOrImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a | b
        super().__init__(register_out, input_a, input_b, operation)


class AssignmentRegisters(ThreeValueInstruction):
    def __init__(
        self, register_in: int, throwaway_value: int, register_out: int
    ) -> None:
        input_a = RegisterOrImmediate(register_in, is_register=True)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(register_out, input_a, input_b, operation)


class AssignmentImmediate(ThreeValueInstruction):
    def __init__(self, value_in: int, throwaway_value: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_in, is_register=False)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanImmediateRegister(ThreeValueInstruction):
    def __init__(self, value_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanRegisterImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class GreaterThanRegisterRegister(ThreeValueInstruction):
    def __init__(self, register_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualImmediateRegister(ThreeValueInstruction):
    def __init__(self, value_a: int, register_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualRegisterImmediate(ThreeValueInstruction):
    def __init__(self, register_a: int, value_b: int, register_out: int) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(register_out, input_a, input_b, operation)


class EqualRegisterRegister(ThreeValueInstruction):
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
    instruction: ThreeValueInstruction,
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
    candidates: list[type[ThreeValueInstruction]],
) -> Iterator[type[ThreeValueInstruction]]:
    for candidate in candidates:
        instruction = candidate(*instruction_sample.instruction_values)
        if _instruction_matches_result(instruction, instruction_sample):
            yield candidate


def work_out_op_codes(
    samples: list[InstructionSample],
    candidates: list[type[ThreeValueInstruction]],
) -> dict[int, type[ThreeValueInstruction]]:
    op_code_to_possible_instructions = _op_code_to_possible_instructions(
        samples, candidates
    )
    num_op_codes = len(op_code_to_possible_instructions)

    op_code_to_instruction = dict()
    while len(op_code_to_instruction) < num_op_codes:
        _disambiguate_next_instruction(
            op_code_to_possible_instructions,
            op_code_to_instruction,
        )

    return op_code_to_instruction


def _op_code_to_possible_instructions(
    samples: list[InstructionSample],
    candidates: list[type[ThreeValueInstruction]],
) -> dict[int, list[type[ThreeValueInstruction]]]:
    op_with_candidates = dict()
    for sample in samples:
        instruction_candidates = op_with_candidates.get(sample.op_code, candidates)
        reduced_candidates = list(possible_instructions(sample, instruction_candidates))
        op_with_candidates[sample.op_code] = reduced_candidates
    return op_with_candidates


def _disambiguate_next_instruction(
    op_code_to_possible_instructions: dict[int, list[type[ThreeValueInstruction]]],
    op_code_to_instruction: dict[int, type[ThreeValueInstruction]],
) -> None:
    instruction = None
    for op_code, possible_candidates in op_code_to_possible_instructions.items():
        if op_code in op_code_to_instruction or len(possible_candidates) > 1:
            continue
        if len(possible_candidates) == 0:
            raise ValueError(f"No candidates for op code {op_code}")
        instruction = possible_candidates[0]
        break

    if instruction is None:
        raise ValueError("Cannot determine any more op codes")

    op_code_to_instruction[op_code] = instruction
    del op_code_to_possible_instructions[op_code]
    for candidates in op_code_to_possible_instructions.values():
        if instruction in candidates:
            candidates.remove(instruction)
