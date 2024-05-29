from ..molecule import (
    molecules_after_one_replacement,
    Molecule,
    num_replacements_from_atom_to_molecule,
)


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


def test_can_find_the_number_of_replacements_to_convert_atom_to_molecule():
    atom = "e"
    molecule = Molecule(("H", "O", "H", "O"))
    replacements = {
        "H": (Molecule(("H", "O")), Molecule(("O", "H"))),
        "O": (Molecule(("H", "H")),),
        "e": (Molecule(("H",)), Molecule(("O",))),
    }
    assert 4 == num_replacements_from_atom_to_molecule(atom, molecule, replacements)
