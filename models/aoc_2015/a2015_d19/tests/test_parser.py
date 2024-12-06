from models.common.io import InputFromString

from ..molecule import Molecule
from ..parser import parse_molecule_replacements


def test_parse_molecule_replacements():
    file_content = """H => HO
                      H => OH
                      O => HH

                      HOH"""
    molecule, replacements = parse_molecule_replacements(InputFromString(file_content))
    assert replacements == {
        "H": (Molecule(("H", "O")), Molecule(("O", "H"))),
        "O": (Molecule(("H", "H")),),
    }
    assert molecule == Molecule(("H", "O", "H"))
