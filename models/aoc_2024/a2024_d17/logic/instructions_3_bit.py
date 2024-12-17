from dataclasses import dataclass

from models.common.assembly import Hardware


def _combo_operand(operand: int, hardware: Hardware) -> int:
    if operand < 4:
        return operand
    else:
        register = chr(ord("A") + operand - 4)
        return hardware.get_value_at_register(register)


@dataclass(frozen=True)
class Division3BitInstruction:
    numerator_register: chr
    output_register: chr
    operand: int

    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter += 2
        numerator = hardware.get_value_at_register(self.numerator_register)
        divisor = 2 ** _combo_operand(self.operand, hardware)
        result = numerator // divisor
        hardware.set_value_at_register(self.output_register, result)


@dataclass(frozen=True)
class XorLiteral3BitInstruction:
    register: chr
    literal: int

    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter += 2
        value = hardware.get_value_at_register(self.register)
        result = value ^ self.literal
        hardware.set_value_at_register(self.register, result)


@dataclass(frozen=True)
class XorRegisters3BitInstruction:
    register_a: chr
    register_b: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter += 2
        value_a = hardware.get_value_at_register(self.register_a)
        value_b = hardware.get_value_at_register(self.register_b)
        result = value_a ^ value_b
        hardware.set_value_at_register(self.register_a, result)


@dataclass(frozen=True)
class Modulo3BitInstruction:
    output_register: chr
    operand: int
    modulo: int

    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter += 2
        numerator = _combo_operand(self.operand, hardware)
        result = numerator % self.modulo
        hardware.set_value_at_register(self.output_register, result)


@dataclass(frozen=True)
class JumpNotZero3BitInstruction:
    register: chr
    new_pc: int

    def execute(self, hardware: Hardware) -> None:
        value = hardware.get_value_at_register(self.register)
        if value != 0:
            hardware.processor.program_counter = self.new_pc
        else:
            hardware.processor.program_counter += 2


@dataclass(frozen=True)
class Output3BitInstruction:
    operand: int
    modulo: int

    def execute(self, hardware: Hardware) -> None:
        hardware.processor.program_counter += 2
        value = _combo_operand(self.operand, hardware)
        result = value % self.modulo
        hardware.serial_output.write(result)
