from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .ferry_seats import FerrySeat, FerrySeats


def aoc_2020_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 11, "Seating System")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())

    ferry_adjacent_only = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=3,
        consider_only_adjacent_neighbors=True,
    )
    final_state = ferry_adjacent_only.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    yield ProblemSolution(
        problem_id,
        f"Occupied seats considering only adjacent neighbors: {num_occupied}",
        part=1,
        result=num_occupied,
    )

    ferry_first_chair = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=4,
        consider_only_adjacent_neighbors=False,
    )
    final_state = ferry_first_chair.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    yield ProblemSolution(
        problem_id,
        f"Occupied seats considering first chair in line of sight: {num_occupied}",
        part=2,
        result=num_occupied,
    )
