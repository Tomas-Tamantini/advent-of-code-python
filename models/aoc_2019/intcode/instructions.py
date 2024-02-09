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
