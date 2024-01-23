def contains_exactly_n_of_any_letter(string: str, n: int) -> bool:
    return any(string.count(letter) == n for letter in string)
