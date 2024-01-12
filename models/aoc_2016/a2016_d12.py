def run_parsed_assembly_code(
    c_register_cpy: int,
    d_register_cpy: int,
    c_multiplier: int,
    d_multiplier: int,
    c_starts_as_one: bool,
) -> int:
    # Assembly code was parsed by hand and simplified to the following:
    num_steps = d_register_cpy + int(c_starts_as_one) * c_register_cpy
    return nth_fibonacci(num_steps + 2) + c_multiplier * d_multiplier


def nth_fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = a + b, a
    return a
