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
                self.destination, hardware.processor.get_value(self.source)
            )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class AddInstruction:
    source: Union[chr, int]
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.increment_value_at_register(
            self.destination, hardware.processor.get_value(self.source)
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class _JumpInstruction:
    offset: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        raise NotImplementedError("This method should be implemented by subclasses")

    def execute(self, hardware: Hardware) -> None:
        if self._should_jump(hardware.processor):
            hardware.increment_program_counter(
                hardware.processor.get_value(self.offset)
            )
        else:
            hardware.increment_program_counter()


@dataclass(frozen=True)
class JumpNotZeroInstruction(_JumpInstruction):
    value_to_compare: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value(self.value_to_compare) != 0


@dataclass(frozen=True)
class JumpGreaterThanZeroInstruction(_JumpInstruction):
    value_to_compare: Union[chr, int]

    def _should_jump(self, processor: Processor) -> bool:
        return processor.get_value(self.value_to_compare) > 0


@dataclass(frozen=True)
class OutInstruction:
    source: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        hardware.serial_output.write(hardware.get_value_at_register(self.source))
        hardware.increment_program_counter()


class NoOpInstruction:
    def execute(self, hardware: Hardware) -> None:
        hardware.increment_program_counter()
