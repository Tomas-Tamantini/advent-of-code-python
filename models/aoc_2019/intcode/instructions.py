from dataclasses import dataclass
from enum import Enum
from models.assembly import Hardware


class ParameterMode(int, Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


@dataclass(frozen=True)
class IntcodeParameter:
    value: int
    parameter_mode: ParameterMode

    def get_position(self, hardware: Hardware) -> int:
        if self.parameter_mode == ParameterMode.POSITION:
            return self.value
        elif self.parameter_mode == ParameterMode.RELATIVE:
            return hardware.relative_base + self.value
        else:
            raise ValueError("Immediate mode does not have a position")

    def get_value(self, hardware: Hardware) -> int:
        if self.parameter_mode == ParameterMode.IMMEDIATE:
            return self.value
        else:
            return hardware.memory.read(address=self.get_position(hardware))


@dataclass(frozen=True)
class IntcodeHalt:
    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter = -1


@dataclass(frozen=True)
class IntcodeAdd:
    input_a: IntcodeParameter
    input_b: IntcodeParameter
    output: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        hardware.memory.write(self.output.get_position(hardware), a + b)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeMultiply:
    input_a: IntcodeParameter
    input_b: IntcodeParameter
    output: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        hardware.memory.write(self.output.get_position(hardware), a * b)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeInput:
    output: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        value = hardware.serial_input.read()
        hardware.memory.write(self.output.get_position(hardware), value)
        hardware.increment_program_counter(increment=2)


@dataclass(frozen=True)
class IntcodeOutput:
    value: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        value = self.value.get_value(hardware)
        hardware.serial_output.write(value)
        hardware.increment_program_counter(increment=2)


@dataclass(frozen=True)
class IntcodeJumpIfTrue:
    condition: IntcodeParameter
    jump_address: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        condition = self.condition.get_value(hardware)
        if condition != 0:
            hardware.processor.program_counter = self.jump_address.get_value(hardware)
        else:
            hardware.increment_program_counter(increment=3)


@dataclass(frozen=True)
class IntcodeJumpIfFalse:
    condition: IntcodeParameter
    jump_address: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        condition = self.condition.get_value(hardware)
        if condition == 0:
            hardware.processor.program_counter = self.jump_address.get_value(hardware)
        else:
            hardware.increment_program_counter(increment=3)


@dataclass(frozen=True)
class IntcodeLessThan:
    input_a: IntcodeParameter
    input_b: IntcodeParameter
    output: IntcodeParameter

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        write_value = 1 if a < b else 0
        hardware.memory.write(self.output.get_position(hardware), write_value)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeEquals:
    input_a: IntcodeParameter
    input_b: IntcodeParameter
    output: int

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        write_value = 1 if a == b else 0
        hardware.memory.write(self.output.get_position(hardware), write_value)
        hardware.increment_program_counter(increment=4)
