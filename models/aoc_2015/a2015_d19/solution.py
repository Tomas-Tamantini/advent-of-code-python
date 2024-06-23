from models.common.io import IOHandler, Problem
from .parser import parse_molecule_replacements
from .molecule import (
    molecules_after_one_replacement,
    num_replacements_from_atom_to_molecule,
)


def aoc_2015_d19(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 19, "Medicine for Rudolph")
    io_handler.output_writer.write_header(problem_id)
    molecule, replacements = parse_molecule_replacements(io_handler.input_reader)
    new_molecules = set(molecules_after_one_replacement(molecule, replacements))
    print(f"Part 1: There are {len(new_molecules)} new molecules after one replacement")
    num_replacements = num_replacements_from_atom_to_molecule(
        "e", molecule, replacements
    )
    print(
        f"Part 2: Minimum number of replacements to make molecule is {num_replacements}"
    )
