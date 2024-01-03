def next_look_and_say(current_term: str) -> str:
    current_digit = current_term[0]
    current_count = 1
    digits_next_term = []
    for digit in current_term[1:]:
        if digit == current_digit:
            current_count += 1
        else:
            digits_next_term.extend((current_count, current_digit))
            current_count = 1
            current_digit = digit
    digits_next_term.extend((current_count, current_digit))
    return "".join(map(str, digits_next_term))
