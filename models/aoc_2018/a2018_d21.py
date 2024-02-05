def optimized_chronal_conversion(input_num: int, exit_on_first_occurrence: bool) -> int:
    visited = set()
    max_num_attempts = 1000
    a = 0
    last_a = -1
    while True:
        b = a | 0x10000
        a = input_num
        while True:
            c = b & 0xFF
            a += c
            a &= 0xFFFFFF
            a *= 65899
            a &= 0xFFFFFF
            if 256 > b:
                if exit_on_first_occurrence:
                    return a
                else:
                    if a not in visited:
                        visited.add(a)
                        last_a = a
                        max_num_attempts = 1000
                    else:
                        max_num_attempts -= 1
                        if max_num_attempts == 0:
                            return last_a
                    break
            b = b // 256
