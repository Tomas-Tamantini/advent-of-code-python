from models.assembly import Instruction, Hardware, Computer, Processor
from .game_console_program import GameConsoleProgram


def run_game_console(instructions: list[Instruction]) -> int:
    hardware = Hardware(processor=Processor(), global_accumulator=0)
    program = GameConsoleProgram(instructions)
    computer = Computer(hardware)
    try:
        computer.run_program(program)
    except GameConsoleProgram.RepeatedInstructionError:
        return hardware.global_accumulator
