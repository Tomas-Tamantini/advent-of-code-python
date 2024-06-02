from dataclasses import dataclass
from typing import Callable, Iterator, Optional
from models.common.assembly import Hardware


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
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        self._register_out = register_out
        self._input_a = input_a
        self._input_b = input_b
        self._operation = operation
        self._register_bound_to_pc = register_bound_to_pc

    def registers_used(self) -> Iterator[int]:
        if self._input_a.is_register:
            yield self._input_a.value
        if self._input_b.is_register:
            yield self._input_b.value
        yield self._register_out

    def execute(self, hardware: Hardware) -> None:
        if self._register_bound_to_pc is not None:
            hardware.set_value_at_register(
                self._register_bound_to_pc, hardware.processor.program_counter
            )
        result = self._operation(
            self._input_a.get_value(hardware),
            self._input_b.get_value(hardware),
        )
        hardware.set_value_at_register(self._register_out, result)
        if self._register_bound_to_pc is not None:
            hardware.processor.program_counter = hardware.get_value_at_register(
                self._register_bound_to_pc
            )
        hardware.increment_program_counter()


class AddRegisters(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a + b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class AddImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a + b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class MultiplyRegisters(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a * b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class MultiplyImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a * b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class BitwiseAndRegisters(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a & b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class BitwiseAndImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a & b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class BitwiseOrRegisters(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: a | b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class BitwiseOrImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: a | b
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class AssignmentRegisters(ThreeValueInstruction):
    def __init__(
        self,
        register_in: int,
        throwaway_value: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_in, is_register=True)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class AssignmentImmediate(ThreeValueInstruction):
    def __init__(
        self,
        value_in: int,
        throwaway_value: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(value_in, is_register=False)
        input_b = RegisterOrImmediate(throwaway_value, is_register=False)
        operation = lambda a, _: a
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class GreaterThanImmediateRegister(ThreeValueInstruction):
    def __init__(
        self,
        value_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class GreaterThanRegisterImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class GreaterThanRegisterRegister(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a > b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class EqualImmediateRegister(ThreeValueInstruction):
    def __init__(
        self,
        value_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(value_a, is_register=False)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class EqualRegisterImmediate(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        value_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(value_b, is_register=False)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


class EqualRegisterRegister(ThreeValueInstruction):
    def __init__(
        self,
        register_a: int,
        register_b: int,
        register_out: int,
        register_bound_to_pc: Optional[int] = None,
    ) -> None:
        input_a = RegisterOrImmediate(register_a, is_register=True)
        input_b = RegisterOrImmediate(register_b, is_register=True)
        operation = lambda a, b: 1 if a == b else 0
        super().__init__(
            register_out, input_a, input_b, operation, register_bound_to_pc
        )


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
