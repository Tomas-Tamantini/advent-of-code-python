def _extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0

    gcd, x, y = _extended_euclidean_algorithm(b, a % b)
    return gcd, y, x - (a // b) * y


def modular_inverse(a: int, mod: int) -> int:
    gcd, x, _ = _extended_euclidean_algorithm(a, mod)
    if gcd != 1:
        raise ValueError(f"{a} has no modular inverse modulo {mod}")
    return x % mod
