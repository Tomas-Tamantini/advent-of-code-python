from math import sqrt, ceil


def modular_logarithm(number: int, base: int, mod: int) -> int:
    # Baby-step giant-step algorithm
    m = ceil(sqrt(mod)) + 1
    table = {pow(base, i, mod): i for i in range(m)}
    base_inv_m = pow(base, mod - m - 1, mod)
    for j in range(m):
        y = (number * pow(base_inv_m, j, mod)) % mod
        if y in table:
            return j * m + table[y]
    raise ValueError(
        f"Could not find a solution for {number} in base {base} modulo {mod}"
    )
