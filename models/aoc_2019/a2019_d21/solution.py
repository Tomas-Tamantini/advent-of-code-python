from models.common.io import IOHandler
from .logic import (
    run_spring_droid_program,
    SpringScriptInstruction,
    SpringScriptInstructionType,
    SpringDroidInput,
    SpringDroidOutput,
    BeginDroidCommand,
)


def aoc_2019_d21(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 21: Springdroid Adventure ---")
    intcode_instructions = [
        int(code) for code in io_handler.input_reader.read().split(",")
    ]
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.WALK
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        print(f"Part 1: Hull damage from walking on the hull is {hull_damage}")
    except ValueError:
        print(droid_output.render())
        print("Part 1: Spring bot fell into a hole. Try a different springscript.")
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "B", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "C", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "D", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.AND, "H", "J"),
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "T"),
        SpringScriptInstruction(SpringScriptInstructionType.OR, "T", "J"),
    ]
    droid_input = SpringDroidInput(
        springscript_instructions, begin_droid_command=BeginDroidCommand.RUN
    )
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    try:
        hull_damage = droid_output.large_output()
        print(f"Part 2: Hull damage from running on the hull is {hull_damage}")
    except ValueError:
        print(droid_output.render())
        print("Part 2: Spring bot fell into a hole. Try a different springscript.")
