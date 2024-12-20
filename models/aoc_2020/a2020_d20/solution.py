from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import solve_jigsaw
from .parser import parse_jigsaw_pieces


def aoc_2020_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 20, "Jurassic Jigsaw")
    io_handler.output_writer.write_header(problem_id)
    pieces = list(parse_jigsaw_pieces(io_handler.input_reader))
    solved_jigsaw = solve_jigsaw(pieces)
    border_pieces = list(solved_jigsaw.border_pieces())
    product = 1
    for piece in border_pieces:
        product *= piece.piece_id
    yield ProblemSolution(
        problem_id, f"Product of corner pieces is {product}", part=1, result=product
    )

    sea_monster_text = "\n".join(
        [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   ",
        ]
    )
    sea_monster = CharacterGrid(text=sea_monster_text.replace(" ", "."))
    monster_positions = set(sea_monster.positions_with_value("#"))
    matches = list(solved_jigsaw.find_pattern_matches(monster_positions))
    num_sea_monster_cells = len(monster_positions) * len(matches)
    num_hash_cells = sum(
        1 for cell in solved_jigsaw.render_as_matrix().flatten() if cell
    )
    num_non_sea_monster_cells = num_hash_cells - num_sea_monster_cells
    yield ProblemSolution(
        problem_id,
        f"Number of non-sea-monster cells is {num_non_sea_monster_cells}",
        part=2,
        result=num_non_sea_monster_cells,
    )
