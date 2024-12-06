from copy import deepcopy
from fractions import Fraction


# TODO: Refactor to reduce cognitive complexity
def solve_linear_system_exactly(a: list[list[int]], b: list[int]) -> list[Fraction]:
    a = deepcopy(a)
    b = deepcopy(b)
    # Solve using Gaussian elimination
    n = len(b)
    for p in range(n):
        # Find pivot row and swap
        aux_max = p
        for i in range(p + 1, n):
            if abs(a[i][p]) > abs(a[aux_max][p]):
                aux_max = i

        for i in range(n):
            a[p][i], a[aux_max][i] = a[aux_max][i], a[p][i]

        b[aux_max], b[p] = b[p], b[aux_max]

        if a[p][p] == 0:
            raise ValueError("Singular matrix cannot be solved")

        # Pivot within a and b
        for i in range(p + 1, n):
            multiplier = Fraction(a[i][p], a[p][p])
            b[i] -= multiplier * b[p]
            for j in range(p, n):
                a[i][j] -= multiplier * a[p][j]

    # Back substitution
    x = [0] * n
    for i in reversed(range(n)):
        acc = sum(a[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - acc) / a[i][i]

    return x
