from typing import Protocol, Union
from dataclasses import dataclass
from .hardware import Hardware, Processor


class Instruction(Protocol):
    def execute(self, hardware: Hardware) -> None:
        ...


# Common instructions:
@dataclass(frozen=True)
class CopyInstruction:
    source: Union[chr, int]
    destination: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if not isinstance(self.destination, int):
            hardware.set_value_at_register(
                self.destination, hardware.processor.get_value_or_immediate(self.source)
            )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class UpdateRegisterInstruction:
    source: Union[chr, int]
    destination: chr

    def _value_source(self, processor: Processor) -> int:
        return processor.get_value_or_immediate(self.source)

    def _value_destination(self, processor: Processor) -> int:
        return processor.get_value_or_immediate(self.destination)

    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        raise NotImplementedError("This method should be implemented by subclasses")

    def execute(self, hardware: Hardware) -> None:
        hardware.set_value_at_register(
            self.destination,
            self._updated_value(
                value_source=self._value_source(hardware.processor),
                value_destination=self._value_destination(hardware.processor),
            ),
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class AddInstruction(UpdateRegisterInstruction):
    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        return value_source + value_destination


@dataclass(frozen=True)
class SubtractInstruction(UpdateRegisterInstruction):
    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        return value_destination - value_source


@dataclass(frozen=True)
class _JumpInstruction:
    offset: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        raise NotImplementedError("This method should be implemented by subclasses")

    def execute(self, hardware: Hardware) -> None:
        if self._should_jump(hardware.processor):
            hardware.increment_program_counter(
                hardware.processor.get_value_or_immediate(self.offset)
            )
        else:
            hardware.increment_program_counter()


@dataclass(frozen=True)
class JumpNotZeroInstruction(_JumpInstruction):
    value_to_compare: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value_or_immediate(self.value_to_compare) != 0


@dataclass(frozen=True)
class JumpGreaterThanZeroInstruction(_JumpInstruction):
    value_to_compare: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value_or_immediate(self.value_to_compare) > 0


@dataclass(frozen=True)
class InputInstruction:
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.set_value_at_register(self.destination, hardware.serial_input.read())
        hardware.increment_program_counter()


@dataclass(frozen=True)
class OutInstruction:
    source: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        hardware.serial_output.write(
            hardware.processor.get_value_or_immediate(self.source)
        )
        hardware.increment_program_counter()


class NoOpInstruction:
    def execute(self, hardware: Hardware) -> None:
        hardware.increment_program_counter()
