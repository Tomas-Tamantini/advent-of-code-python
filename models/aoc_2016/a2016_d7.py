def ip_supports_tls(ip: str) -> bool:
    contains_abba_like_sequence = False
    is_inside_bracket = False
    for i, c in enumerate(ip):
        if i >= len(ip) - 3:
            break
        if c == "[":
            is_inside_bracket = True
        elif c == "]":
            is_inside_bracket = False
        else:
            if c == ip[i + 3] and ip[i + 1] == ip[i + 2] and c != ip[i + 1]:
                contains_abba_like_sequence = True
                if is_inside_bracket:
                    return False
    return contains_abba_like_sequence
