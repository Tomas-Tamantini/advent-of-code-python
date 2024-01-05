from models.aoc_2015 import molecule_replacements


def test_molecule_replacements_returns_all_possible_molecules_after_one_replacement():
    replacements = {
        "H": ("HO", "OH"),
        "O": ("HH",),
    }
    assert {"HOOH", "HOHO", "OHOH", "HHHH"} == set(
        molecule_replacements("HOH", replacements)
    )
