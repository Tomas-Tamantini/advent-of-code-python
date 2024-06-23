from hashlib import md5
from models.common.io import IOHandler, Problem, ProblemSolution


def md5_hash(message: str) -> str:
    return md5(message.encode()).hexdigest()


def mine_advent_coins(secret_key: str, num_leading_zeros: int) -> int:
    number = 0
    starting_zeros = "0" * num_leading_zeros
    while True:
        number += 1
        message = secret_key + str(number)
        hashed_message = md5_hash(message)
        if hashed_message.startswith(starting_zeros):
            return number


def aoc_2015_d4(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 4, "The Ideal Stocking Stuffer")
    io_handler.output_writer.write_header(problem_id)
    secret_key = io_handler.input_reader.read()
    result = mine_advent_coins(secret_key, num_leading_zeros=5)
    solution = ProblemSolution(
        problem_id,
        f"The number to make hash start with 5 zeroes is {result}",
        result,
        part=1,
    )
    io_handler.set_solution(solution)

    result = mine_advent_coins(secret_key, num_leading_zeros=6)
    solution = ProblemSolution(
        problem_id,
        f"The number to make hash start with 6 zeroes is {result}",
        result,
        part=2,
    )
    io_handler.set_solution(solution)
