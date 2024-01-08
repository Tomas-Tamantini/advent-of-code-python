from models.aoc_2015 import molecules_after_one_replacement, Molecule


def test_molecule_replacements_returns_all_possible_molecules_after_one_replacement():
    molecule_hoh = Molecule(("H", "O", "H"))
    replacements = {
        "H": (Molecule(("H", "O")), Molecule(("O", "H"))),
        "O": (Molecule(("H", "H")),),
    }
    expected_molecules = {
        Molecule(("H", "O", "O", "H")),
        Molecule(("H", "O", "H", "O")),
        Molecule(("O", "H", "O", "H")),
        Molecule(("H", "H", "H", "H")),
    }
    assert expected_molecules == set(
        molecules_after_one_replacement(molecule_hoh, replacements)
    )
