from dataclasses import dataclass
from typing import Iterator
from models.assembly import Hardware, Processor, Computer
from models.aoc_2019.intcode import IntcodeProgram
from .network_router import NetworkRouter
from .network_output import NetworkOutput
from .lost_packets import LostPackets


@dataclass
class _ComputerState:
    computer: Computer
    program: IntcodeProgram
    is_halted: bool = False


def _computer_states(
    router: NetworkRouter, instructions: list[int]
) -> Iterator[_ComputerState]:
    for i in range(router.num_computers):
        processor = Processor()
        program = IntcodeProgram(instructions[:])
        serial_input = router.network_input(address=i)
        serial_output = NetworkOutput(router)
        hardware = Hardware(
            processor=processor,
            memory=program,
            serial_input=serial_input,
            serial_output=serial_output,
            relative_base=0,
        )
        computer = Computer(hardware)
        yield _ComputerState(computer, program)


def run_network_until_bad_address(
    num_computers: int, lost_packets_manager: LostPackets, instructions: list[int]
) -> None:
    router = NetworkRouter(num_computers, lost_packets_manager)
    computers = list(_computer_states(router, instructions))
    while True:
        for computer_state in computers:
            if computer_state.is_halted:
                continue
            try:
                computer_state.computer.run_next_instruction(computer_state.program)
            except StopIteration:
                computer_state.is_halted = True
            if lost_packets_manager.received_packet:
                return


def run_network_until_y_overflow(
    num_computers: int, lost_packets_manager: LostPackets, instructions: list[int]
) -> None:
    router = NetworkRouter(num_computers, lost_packets_manager)
    computers = list(_computer_states(router, instructions))
    while True:
        if router.is_idle():
            try:
                router.resend_lost_packet()
            except OverflowError:
                return
        for computer_state in computers:
            if computer_state.is_halted:
                continue
            try:
                computer_state.computer.run_next_instruction(computer_state.program)
            except StopIteration:
                computer_state.is_halted = True
