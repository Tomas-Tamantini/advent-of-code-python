from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import HexagonalDirection, CanonicalHexagonalCoordinates


def aoc_2017_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 11, "Hex Ed")
    io_handler.output_writer.write_header(problem_id)
    directions = [
        HexagonalDirection(d) for d in io_handler.input_reader.read().strip().split(",")
    ]
    pos = CanonicalHexagonalCoordinates(0, 0)
    steps_away = []
    for direction in directions:
        pos = pos.move(direction)
        steps_away.append(pos.num_steps_away_from_origin())
    yield ProblemSolution(
        problem_id,
        f"He ended up {steps_away[-1]} steps away",
        part=1,
        result=steps_away[-1],
    )

    yield ProblemSolution(
        problem_id,
        f"He was at most {max(steps_away)} steps away",
        part=2,
        result=max(steps_away),
    )
