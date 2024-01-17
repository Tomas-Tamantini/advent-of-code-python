def stream_groups_total_score(stream: str) -> int:
    total_score = 0
    current_score = 0
    is_inside_garbage = False
    char_idx = 0
    while char_idx < len(stream):
        c = stream[char_idx]
        if c == "!":
            char_idx += 2
            continue
        elif c == "<":
            is_inside_garbage = True
        elif c == ">":
            is_inside_garbage = False
        elif c == "{" and not is_inside_garbage:
            current_score += 1
            total_score += current_score
        elif c == "}" and not is_inside_garbage:
            current_score -= 1
        char_idx += 1
    return total_score
