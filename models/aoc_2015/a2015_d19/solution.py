from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .molecule import (
    molecules_after_one_replacement,
    num_replacements_from_atom_to_molecule,
)
from .parser import parse_molecule_replacements


def aoc_2015_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 19, "Medicine for Rudolph")
    io_handler.output_writer.write_header(problem_id)
    molecule, replacements = parse_molecule_replacements(io_handler.input_reader)
    new_molecules = set(molecules_after_one_replacement(molecule, replacements))
    yield ProblemSolution(
        problem_id,
        f"There are {len(new_molecules)} new molecules after one replacement",
        part=1,
        result=len(new_molecules),
    )

    num_replacements = num_replacements_from_atom_to_molecule(
        "e", molecule, replacements
    )
    yield ProblemSolution(
        problem_id,
        f"Minimum number of replacements to make molecule is {num_replacements}",
        part=2,
        result=num_replacements,
    )
