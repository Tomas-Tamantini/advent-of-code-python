from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_encrypted_rooms


def aoc_2016_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 4, "Security Through Obscurity")
    io_handler.output_writer.write_header(problem_id)
    id_sum = 0
    id_storage = -1
    for room in parse_encrypted_rooms(io_handler.input_reader):
        if room.is_real():
            id_sum += room.sector_id
            if "pole" in room.decrypt_name():
                id_storage = room.sector_id
    yield ProblemSolution(
        problem_id, f"Sum of sector IDs of real rooms: {id_sum}", part=1, result=id_sum
    )

    yield ProblemSolution(
        problem_id,
        f"Sector ID of room where North Pole objects are stored: {id_storage}",
        result=id_storage,
        part=2,
    )
