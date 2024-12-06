from dataclasses import dataclass
from typing import Iterator

from models.aoc_2019.intcode import IntcodeProgram
from models.common.assembly import Computer, Hardware, Processor

from .lost_packets import LostPackets
from .network_output import NetworkOutput
from .network_router import NetworkRouter
from .packet_monitor import HaltNetworkError


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


def run_network(
    num_computers: int, lost_packets_manager: LostPackets, instructions: list[int]
) -> None:
    router = NetworkRouter(num_computers, lost_packets_manager)
    computers = list(_computer_states(router, instructions))
    while True:
        if router.is_idle():
            try:
                router.resend_lost_packet()
            except HaltNetworkError:
                return
        for computer_state in computers:
            if computer_state.is_halted:
                continue
            try:
                computer_state.computer.run_next_instruction(computer_state.program)
            except StopIteration:
                computer_state.is_halted = True
            except HaltNetworkError:
                return
