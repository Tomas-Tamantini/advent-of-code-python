class StreamHandler:
    def __init__(self, stream: str) -> None:
        self._total_score = 0
        self._num_non_cancelled_chars_in_garbage = 0
        self._parse_stream(stream)

    def _parse_stream(self, stream: str) -> None:
        current_score = 0
        is_inside_garbage = False
        char_idx = 0
        while char_idx < len(stream):
            c = stream[char_idx]
            if c == "!":
                char_idx += 2
                continue
            if is_inside_garbage:
                self._num_non_cancelled_chars_in_garbage += 1
            if c == "<":
                is_inside_garbage = True
            elif c == ">":
                if is_inside_garbage:
                    is_inside_garbage = False
                    self._num_non_cancelled_chars_in_garbage -= 1
                else:
                    raise ValueError("Found '>' outside garbage")
            elif c == "{" and not is_inside_garbage:
                current_score += 1
                self._total_score += current_score
            elif c == "}" and not is_inside_garbage:
                current_score -= 1
            char_idx += 1

    @property
    def total_score(self) -> int:
        return self._total_score

    @property
    def num_non_cancelled_chars_in_garbage(self) -> int:
        return self._num_non_cancelled_chars_in_garbage
