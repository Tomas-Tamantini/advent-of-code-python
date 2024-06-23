from models.common.io import IOHandler
from models.common.assembly import InputInstruction
from .parser import parse_duet_code
from .duet_code import last_recovered_frequency, sent_values_in_two_way_communication


def aoc_2017_d18(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2017, 18, "Duet")
    instructions_audio = list(parse_duet_code(io_handler.input_reader))
    audio_output = last_recovered_frequency(instructions_audio)
    print(f"Part 1: Last recovered frequency: {audio_output}")
    instructions_communication = list(
        parse_duet_code(io_handler.input_reader, rcv_cls=InputInstruction)
    )
    sent_values = sent_values_in_two_way_communication(instructions_communication)

    print(f"Part 2: Number of values sent by program 1: {len(sent_values['1'])}")
