from models.common.io import IOHandler, Problem


def aoc_2015_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 23, "Opening the Turing Lock")
    io_handler.output_writer.write_header(problem_id)
    # TODO: Make implementation independent of input
    print(
        "Part 1: Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 20895 to 1: 255 "
    )
    print(
        "Part 2: Done by hand (it's just 3n+1 problem in disguise) - Num. steps to go from 60975 to 1: 334"
    )
