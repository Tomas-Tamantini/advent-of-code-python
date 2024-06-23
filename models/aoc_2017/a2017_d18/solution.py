from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.assembly import InputInstruction
from .parser import parse_duet_code
from .duet_code import last_recovered_frequency, sent_values_in_two_way_communication


def aoc_2017_d18(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 18, "Duet")
    io_handler.output_writer.write_header(problem_id)
    instructions_audio = list(parse_duet_code(io_handler.input_reader))
    audio_output = last_recovered_frequency(instructions_audio)
    solution = ProblemSolution(
        problem_id, f"Last recovered frequency: {audio_output}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    instructions_communication = list(
        parse_duet_code(io_handler.input_reader, rcv_cls=InputInstruction)
    )
    sent_values = sent_values_in_two_way_communication(instructions_communication)

    solution = ProblemSolution(
        problem_id,
        f"Number of values sent by program 1: {len(sent_values['1'])}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
