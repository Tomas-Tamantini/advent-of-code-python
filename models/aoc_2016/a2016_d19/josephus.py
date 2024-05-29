def josephus(num_players: int) -> int:
    return int(bin(num_players)[3:] + "1", 2)


def _number_base_three(n: int) -> str:
    """Convert a number to base three"""
    if n == 0:
        return ""
    return _number_base_three(n // 3) + str(n % 3)


def modified_josephus(num_players: int) -> int:
    """Game where the elf across the circle is stolen from instead of the one to the left"""
    """This formula was guessed by looking at the results of the first 100 numbers"""
    if num_players < 3:
        return 1
    base_three = _number_base_three(num_players - 1)
    if base_three[0] == "1":
        return 1 + int(base_three[1:], 3)
    else:
        return 2 * num_players - 3 ** (len(base_three))
