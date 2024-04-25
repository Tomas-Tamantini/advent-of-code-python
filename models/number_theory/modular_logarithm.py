def modular_logarithm(number: int, base: int, mod: int) -> int:
    for i in range(mod + 1):
        if pow(base, i, mod) == number:
            return i
    raise ValueError(f"Cannot raise {base} to any power to make {number} mod {mod}")
