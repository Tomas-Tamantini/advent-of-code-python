def num_chars_encoded(string: str) -> int:
    return len(string) + 2 + string.count('"') + string.count("\\")


def num_chars_in_memory(string: str) -> int:
    char_counter = 0
    char_pointer = 1
    while char_pointer < len(string) - 1:
        if string[char_pointer] != "\\":
            char_pointer += 1
        elif string[char_pointer + 1] == "\\" or string[char_pointer + 1] == '"':
            char_pointer += 2
        elif _starts_with_hexadecimal_notation(string[char_pointer + 1 :]):
            char_pointer += 4
        else:
            char_pointer += 1
        char_counter += 1
    return char_counter


def _starts_with_hexadecimal_notation(string: str) -> bool:
    if len(string) < 3 or string[0] != "x":
        return False
    try:
        int(string[1:3], 16)
        return True
    except ValueError:
        return False
