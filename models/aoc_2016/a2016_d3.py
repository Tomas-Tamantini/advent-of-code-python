def is_valid_triangle(side_a: int, side_b: int, side_c: int) -> bool:
    return (
        side_a + side_b > side_c
        and side_a + side_c > side_b
        and side_b + side_c > side_a
    )
