from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_multi_technique_shuffle


def aoc_2019_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 22, "Slam Shuffle")
    io_handler.output_writer.write_header(problem_id)
    shuffle = parse_multi_technique_shuffle(io_handler.input_reader)
    new_position = shuffle.new_card_position(
        position_before_shuffle=2019, deck_size=10_007
    )
    yield ProblemSolution(
        problem_id,
        f"New position of card 2019 is {new_position}",
        part=1,
        result=new_position,
    )

    original_position = shuffle.original_card_position(
        position_after_shuffle=2020,
        deck_size=119315717514047,
        num_shuffles=101741582076661,
    )
    yield ProblemSolution(
        problem_id,
        f"Original position of card 2020 is {original_position}",
        part=2,
        result=original_position,
    )
