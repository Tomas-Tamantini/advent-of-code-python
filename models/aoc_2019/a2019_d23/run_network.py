from dataclasses import dataclass
from typing import Iterator
from models.assembly import Hardware, Processor, Computer
from models.aoc_2019.intcode import IntcodeProgram
from .network_router import NetworkRouter
from .network_output import NetworkOutput


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


def run_network(router: NetworkRouter, instructions: list[int]) -> None:
    computers = list(_computer_states(router, instructions))
    num_halted_computers = 0
    while num_halted_computers < router.num_computers:
        for computer_state in computers:
            if computer_state.is_halted:
                continue
            try:
                computer_state.computer.run_next_instruction(computer_state.program)
            except StopIteration:
                computer_state.is_halted = True
                num_halted_computers += 1
            except NetworkRouter.BadSendAddressError:
                return
