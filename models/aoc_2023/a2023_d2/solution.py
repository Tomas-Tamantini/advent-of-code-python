from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_cube_games
from .logic import CubeAmount


def _power(bag: CubeAmount) -> int:
    amounts = bag.amount_by_color
    return amounts["red"] * amounts["green"] * amounts["blue"]


def aoc_2023_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 2, "Cube Conundrum")
    io_handler.output_writer.write_header(problem_id)
    games = list(parse_cube_games(io_handler.input_reader))
    reference_bag = CubeAmount(amount_by_color={"red": 12, "green": 13, "blue": 14})
    possible_games = [
        game for game in games if game.bag_amount_is_possible(reference_bag)
    ]
    sum_ids = sum(game.game_id for game in possible_games)
    yield ProblemSolution(
        problem_id,
        f"The sum of IDs of possible games is {sum_ids}",
        result=sum_ids,
        part=1,
    )
    sum_powers = sum(_power(game.minimum_bag()) for game in games)
    yield ProblemSolution(
        problem_id,
        f"The sum of powers of minimum bags is {sum_powers}",
        result=sum_powers,
        part=2,
    )
