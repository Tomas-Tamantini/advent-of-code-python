from dataclasses import dataclass
from models.assembly import Hardware


@dataclass(frozen=True)
class MemoryOrImmediate:
    value: int
    is_memory: bool

    def get_value(self, hardware: Hardware) -> int:
        if self.is_memory:
            return hardware.memory.read(address=self.value)
        else:
            return self.value


@dataclass(frozen=True)
class IntcodeHalt:
    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter = -1


@dataclass(frozen=True)
class IntcodeAdd:
    input_a: MemoryOrImmediate
    input_b: MemoryOrImmediate
    output: int

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        hardware.memory.write(self.output, a + b)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeMultiply:
    input_a: MemoryOrImmediate
    input_b: MemoryOrImmediate
    output: int

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        hardware.memory.write(self.output, a * b)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeInput:
    output: int

    def execute(self, hardware: Hardware) -> None:
        value = hardware.serial_input.read()
        hardware.memory.write(self.output, value)
        hardware.increment_program_counter(increment=2)


@dataclass(frozen=True)
class IntcodeOutput:
    value: MemoryOrImmediate

    def execute(self, hardware: Hardware) -> None:
        value = self.value.get_value(hardware)
        hardware.serial_output.write(value)
        hardware.increment_program_counter(increment=2)


@dataclass(frozen=True)
class IntcodeJumpIfTrue:
    condition: MemoryOrImmediate
    jump_address: MemoryOrImmediate

    def execute(self, hardware: Hardware) -> None:
        condition = self.condition.get_value(hardware)
        if condition != 0:
            hardware.processor.program_counter = self.jump_address.get_value(hardware)
        else:
            hardware.increment_program_counter(increment=3)


@dataclass(frozen=True)
class IntcodeJumpIfFalse:
    condition: MemoryOrImmediate
    jump_address: MemoryOrImmediate

    def execute(self, hardware: Hardware) -> None:
        condition = self.condition.get_value(hardware)
        if condition == 0:
            hardware.processor.program_counter = self.jump_address.get_value(hardware)
        else:
            hardware.increment_program_counter(increment=3)


@dataclass(frozen=True)
class IntcodeLessThan:
    input_a: MemoryOrImmediate
    input_b: MemoryOrImmediate
    output: int

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        if a < b:
            hardware.memory.write(self.output, 1)
        else:
            hardware.memory.write(self.output, 0)
        hardware.increment_program_counter(increment=4)


@dataclass(frozen=True)
class IntcodeEquals:
    input_a: MemoryOrImmediate
    input_b: MemoryOrImmediate
    output: int

    def execute(self, hardware: Hardware) -> None:
        a = self.input_a.get_value(hardware)
        b = self.input_b.get_value(hardware)
        if a == b:
            hardware.memory.write(self.output, 1)
        else:
            hardware.memory.write(self.output, 0)
        hardware.increment_program_counter(increment=4)
