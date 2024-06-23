from models.common.io import IOHandler
from .parser import parse_bitmask_instructions
from .bitmask_memory import BitmaskMemory


def aoc_2020_d14(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2020, 14, "Docking Data")
    values_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=False)
    )
    memory = BitmaskMemory()
    for instruction in values_instructions:
        instruction.execute(memory)
    print(
        f"Part 1: Sum of values in memory after applying mask to values is {memory.sum_values()}"
    )

    address_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=True)
    )
    memory = BitmaskMemory()
    for instruction in address_instructions:
        instruction.execute(memory)
    print(
        f"Part 2: Sum of values in memory after applying mask to addresses is {memory.sum_values()}"
    )
