from typing import Optional
from models.progress_bar_protocol import ProgressBar


def modular_logarithm(
    number: int,
    base: int,
    mod: int,
    progress_bar: Optional[ProgressBar] = None,
) -> int:
    for i in range(mod + 1):
        if progress_bar:
            progress_bar.update(i, mod + 1)
        if pow(base, i, mod) == number:
            return i
    raise ValueError(f"Cannot raise {base} to any power to make {number} mod {mod}")
