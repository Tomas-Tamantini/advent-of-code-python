def next_look_and_say(digits_current_term: list[int]) -> list[int]:
    current_digit = digits_current_term[0]
    current_count = 1
    digits_next_term = []
    for digit in digits_current_term[1:]:
        if digit == current_digit:
            current_count += 1
        else:
            digits_next_term.extend([current_count, current_digit])
            current_count = 1
            current_digit = digit
    digits_next_term.extend([current_count, current_digit])
    return digits_next_term
