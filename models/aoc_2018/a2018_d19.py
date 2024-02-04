from math import sqrt


def optimized_sum_divisors_program(a: int, b: int) -> int:
    n_part_1 = 22 * a + b + 836
    n = n_part_1 + 10550400

    sqrt_n = int(sqrt(n))
    return sum(d + n // d for d in range(1, sqrt_n + 1) if n % d == 0) - sqrt_n * (
        sqrt_n * sqrt_n == n
    )
