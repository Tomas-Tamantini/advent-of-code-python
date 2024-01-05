from typing import Iterator


def molecule_replacements(
    molecule: str,
    replacements: dict[str, tuple[str]],
) -> Iterator[str]:
    for pattern, possible_replacements in replacements.items():
        for i in range(len(molecule)):
            if molecule[i : i + len(pattern)] == pattern:
                for replacement in possible_replacements:
                    yield molecule[:i] + replacement + molecule[i + len(pattern) :]
