from models.common.io import IOHandler, Problem
from models.common.number_theory import modular_logarithm


def aoc_2020_d25(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 25, "Combo Breaker")
    io_handler.output_writer.write_header(problem_id)
    public_keys = [int(line.strip()) for line in io_handler.input_reader.readlines()]
    subject_number = 7
    mod = 20201227
    loop_size_card = modular_logarithm(public_keys[0], subject_number, mod)
    loop_size_door = modular_logarithm(public_keys[1], subject_number, mod)
    encryption_key = pow(subject_number, loop_size_card * loop_size_door, mod)
    print(f"Encryption key is {encryption_key}")
