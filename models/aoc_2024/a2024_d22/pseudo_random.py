def next_pseudo_random(current: int) -> int:
    mod_mask = 2**24 - 1
    current ^= current << 6
    current &= mod_mask
    current ^= current >> 5
    current &= mod_mask
    current ^= current << 11
    current &= mod_mask
    return current
