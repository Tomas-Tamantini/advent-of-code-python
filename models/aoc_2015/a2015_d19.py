from typing import Iterator, Optional
from dataclasses import dataclass
from random import shuffle


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

    def has_submolecule(self, submolecule: "Molecule") -> bool:
        for i in range(len(self) - len(submolecule) + 1):
            if self.atoms[i : i + len(submolecule)] == submolecule.atoms:
                return True
        return False

    def replace_first_occurrence(
        self, submolecule: "Molecule", replacement_atom: str
    ) -> "Molecule":
        for i in range(len(self) - len(submolecule) + 1):
            if self.atoms[i : i + len(submolecule)] == submolecule.atoms:
                return Molecule(
                    self.atoms[:i]
                    + (replacement_atom,)
                    + self.atoms[i + len(submolecule) :]
                )
        raise ValueError(f"Submolecule {submolecule} not found in {self}")

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


def num_replacements_from_atom_to_molecule(
    atom: str,
    molecule: Molecule,
    replacements: dict[str, tuple[Molecule]],
) -> int:
    list_replacements = []
    for pattern, possible_replacements in replacements.items():
        for replacement in possible_replacements:
            list_replacements.append((pattern, replacement))
    min_replacements = -1
    list_replacements.sort(key=lambda x: len(x[1]), reverse=True)
    num_rounds_without_improvement = 0
    for _ in range(1_000):
        num_replacements = _try_replacements(atom, molecule, list_replacements)
        if num_replacements is not None:
            if min_replacements == -1 or num_replacements < min_replacements:
                min_replacements = num_replacements
                num_rounds_without_improvement = 0
            else:
                num_rounds_without_improvement += 1
                if num_rounds_without_improvement > 2:
                    break
        shuffle(list_replacements)
    return min_replacements


def _try_replacements(
    atom: str,
    molecule: Molecule,
    list_replacements: list[tuple[str, Molecule]],
) -> Optional[int]:
    num_replacements = 0
    while str(molecule) != atom:
        for pattern, replacement in list_replacements:
            if molecule.has_submolecule(replacement):
                num_replacements += 1
                molecule = molecule.replace_first_occurrence(replacement, pattern)
                break
        else:
            return None
    return num_replacements
