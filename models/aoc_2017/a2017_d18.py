from typing import Union
from dataclasses import dataclass
from models.assembly import (
    Hardware,
    Instruction,
    Computer,
    ImmutableProgram,
    Processor,
    UpdateRegisterInstruction,
)


class _AudioOutput:
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


class _MessageQueue:
    def __init__(self) -> None:
        self._queue = []
        self._sent_values = []

    @property
    def sent_values(self) -> list[int]:
        return self._sent_values

    def write(self, value: int) -> None:
        self._queue.append(value)
        self._sent_values.append(value)

    def read(self) -> int:
        if len(self._queue) == 0:
            raise ValueError("No messages to read")
        return self._queue.pop(0)


@dataclass(frozen=True)
class MultiplyInstruction(UpdateRegisterInstruction):
    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        return value_source * value_destination


@dataclass(frozen=True)
class RemainderInstruction(UpdateRegisterInstruction):
    source: Union[chr, int]
    destination: chr

    @staticmethod
    def _updated_value(value_source: int, value_destination: int) -> int:
        return value_destination % value_source


@dataclass(frozen=True)
class RecoverLastFrequencyInstruction:
    source: Union[chr, int]

    def execute(self, hardware: Hardware) -> None:
        if hardware.processor.get_value(self.source) != 0:
            hardware.serial_output.write(-1)
        hardware.increment_program_counter()


def last_recovered_frequency(instructions: list[Instruction]) -> int:
    audio_output = _AudioOutput()
    hardware = Hardware(processor=Processor(), serial_output=audio_output)
    computer = Computer(hardware)
    program = ImmutableProgram(instructions)
    while True:
        try:
            computer.run_next_instruction(program)
        except StopIteration:
            return audio_output.last_frequency_played


def sent_values_in_two_way_communication(
    instructions: list[Instruction],
) -> dict[str, list[int]]:
    program = ImmutableProgram(instructions)
    message_queue_cp_0 = _MessageQueue()
    message_queue_cp_1 = _MessageQueue()
    hardware_cp_0 = Hardware(
        processor=Processor({"p": 0}),
        serial_output=message_queue_cp_0,
        serial_input=message_queue_cp_1,
    )
    hardware_cp_1 = Hardware(
        processor=Processor({"p": 1}),
        serial_output=message_queue_cp_1,
        serial_input=message_queue_cp_0,
    )
    computers = {
        0: Computer(hardware_cp_0),
        1: Computer(hardware_cp_1),
    }
    computers_in_deadlock = set()
    while len(computers_in_deadlock) < 2:
        for computer_id, computer in computers.items():
            try:
                computer.run_next_instruction(program)
            except ValueError:
                computers_in_deadlock.add(computer_id)
    return {
        "0": message_queue_cp_0.sent_values,
        "1": message_queue_cp_1.sent_values,
    }
