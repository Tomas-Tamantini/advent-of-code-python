from typing import Union
from dataclasses import dataclass
from models.assembly import Hardware, Instruction, Computer, ImmutableProgram, Processor


class AudioOutput:
    def __init__(self) -> None:
        self._last_frequency_played = -1

    @property
    def last_frequency_played(self) -> int:
        return self._last_frequency_played

    def write(self, value: int) -> None:
        if value == -1:
            raise StopIteration(f"Last frequency played: {self._last_frequency_played}")
        else:
            self._last_frequency_played = value


# TODO: Multiply, Remainder and Add instructions are very similar. Maybe create a super class


@dataclass(frozen=True)
class MultiplyInstruction:
    source: Union[chr, int]
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.set_value_at_register(
            self.destination,
            hardware.processor.get_value(self.source)
            * hardware.get_value_at_register(self.destination),
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class RemainderInstruction:
    source: Union[chr, int]
    destination: chr

    def execute(self, hardware: Hardware) -> None:
        hardware.set_value_at_register(
            self.destination,
            hardware.get_value_at_register(self.destination)
            % hardware.processor.get_value(self.source),
        )
        hardware.increment_program_counter()


@dataclass(frozen=True)
class RecoverLastFrequencyInstruction:
    source: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if hardware.processor.get_value(self.source) != 0:
            hardware.serial_output.write(-1)
        hardware.increment_program_counter()


def last_recovered_frequency(instructions: list[Instruction]) -> int:
    audio_output = AudioOutput()
    hardware = Hardware(processor=Processor(), serial_output=audio_output)
    computer = Computer(hardware)
    program = ImmutableProgram(instructions)
    while True:
        try:
            computer.run_next_instruction(program)
        except StopIteration:
            return audio_output.last_frequency_played
