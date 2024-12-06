from models.common.assembly import Computer, Hardware, Instruction, Processor

from .game_console_program import GameConsoleProgram


def run_game_console(instructions: list[Instruction]) -> int:
    hardware = Hardware(processor=Processor(), global_accumulator=0)
    program = GameConsoleProgram(instructions)
    computer = Computer(hardware)
    try:
        computer.run_program(program)
    except GameConsoleProgram.RepeatedInstructionError:
        return hardware.global_accumulator


def find_and_run_game_console_which_terminates(instructions: list[Instruction]) -> int:
    for i in GameConsoleProgram.indices_which_can_be_toggled(instructions):
        program = GameConsoleProgram(instructions, index_to_toggle=i)
        hardware = Hardware(processor=Processor(), global_accumulator=0)
        computer = Computer(hardware)
        try:
            computer.run_program(program)
            return hardware.global_accumulator
        except GameConsoleProgram.RepeatedInstructionError:
            continue
