from typing import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Molecule:
    atoms: tuple[str]

    def __len__(self) -> int:
        return len(self.atoms)

    def __iter__(self) -> Iterator[str]:
        return iter(self.atoms)

    def replace_atom(self, atom_idx: int, replacement: "Molecule") -> "Molecule":
        return Molecule(
            self.atoms[:atom_idx] + replacement.atoms + self.atoms[atom_idx + 1 :]
        )

    def __str__(self) -> str:
        return "".join(self.atoms)


def molecules_after_one_replacement(
    molecule: Molecule,
    replacements: dict[str, tuple[Molecule]],
) -> Iterator[Molecule]:
    for pattern, possible_replacements in replacements.items():
        for i, atom in enumerate(molecule):
            if atom == pattern:
                for replacement in possible_replacements:
                    yield molecule.replace_atom(i, replacement)
