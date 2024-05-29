import re
from models.common.io import InputReader
from .molecule import Molecule


def _parse_molecule(molecule_str: str) -> Molecule:
    atom_pattern = re.compile(r"([A-Z][a-z]?)")
    atoms = re.findall(atom_pattern, molecule_str)
    return Molecule(tuple(atoms))


def parse_molecule_replacements(
    input_reader: InputReader,
) -> tuple[Molecule, dict[str, tuple[Molecule]]]:
    lines = list(input_reader.readlines())
    molecule = _parse_molecule(lines[-1].strip())
    replacements = {}
    for line in lines:
        if "=>" not in line:
            continue
        atom, replace_molecule_str = line.strip().split(" => ")
        if atom not in replacements:
            replacements[atom] = []
        replacements[atom].append(_parse_molecule(replace_molecule_str))
    return molecule, {k: tuple(v) for k, v in replacements.items()}
