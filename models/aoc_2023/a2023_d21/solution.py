from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import BoundedGarden, Gardener, InfiniteGarden


def _extrapolate_parabola(first_terms: tuple[int, int, int], desired_index: int) -> int:
    twice_a = first_terms[0] - 2 * first_terms[1] + first_terms[2]
    twice_b = -3 * first_terms[0] + 4 * first_terms[1] - first_terms[2]
    twice_c = 2 * first_terms[0]
    twice_value = (
        twice_a * desired_index * desired_index + twice_b * desired_index + twice_c
    )
    return twice_value // 2


def aoc_2023_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 21, "Step Counter")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    rock_positions = set(grid.positions_with_value("#"))
    initial_position = next(grid.positions_with_value("S"))
    gardener = Gardener(initial_position)

    bounded_garden = BoundedGarden(grid.width, grid.height, rock_positions)
    series_generator = gardener.num_reachable_positions(bounded_garden)
    series = [next(series_generator) for _ in range(65)]

    num_plots_bounded_garden = series[-1]
    yield ProblemSolution(
        problem_id,
        f"The number of garden plots the gardener can reach in bounded garden is {num_plots_bounded_garden}",
        result=num_plots_bounded_garden,
        part=1,
    )

    infinite_garden = InfiniteGarden(grid.width, grid.height, rock_positions)
    series_generator = gardener.num_reachable_positions(infinite_garden)

    # Solution below assumes that the series grows as a parabola considering terms of the form s[offset + period * i]
    # The period is the size of the garden, but only works for square gardens
    if infinite_garden.width != infinite_garden.height:
        raise NotImplementedError("Algorithm only works for square gardens")

    num_steps = 26501365
    period = infinite_garden.height
    # 3 terms to uniquely determine parabola coefficients
    term_indices = [num_steps % period + period * i for i in range(3)]
    series = [next(series_generator) for _ in range(term_indices[-1] + 1)]
    terms = tuple(series[i] for i in term_indices)
    desired_index = num_steps // period

    num_plots_infinite_garden = _extrapolate_parabola(terms, desired_index)
    yield ProblemSolution(
        problem_id,
        f"The number of garden plots the gardener can reach in infinite garden is {num_plots_infinite_garden}",
        result=num_plots_infinite_garden,
        part=2,
    )
