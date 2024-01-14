def swap_letters(s: str, x: chr, y: chr) -> str:
    return s.replace(x, "_").replace(y, x).replace("_", y)


def swap_positions(s: str, x: int, y: int) -> str:
    return swap_letters(s, s[x], s[y])


def rotate_string(s: str, steps: int) -> str:
    cut = -steps % len(s)
    return s[cut:] + s[:cut]


def rotate_based_on_position_of_letter(s: str, letter: chr) -> str:
    letter_idx = s.index(letter)
    steps = 1 + letter_idx + (1 if letter_idx >= 4 else 0)
    return rotate_string(s, steps)


def reverse_positions(s: str, x: int, y: int) -> str:
    return s[:x] + s[x : y + 1][::-1] + s[y + 1 :]


def move_letter(s: str, x: int, y: int) -> str:
    letter = s[x]
    s = s[:x] + s[x + 1 :]
    return s[:y] + letter + s[y:]
