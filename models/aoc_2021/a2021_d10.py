from typing import Iterator

_open_to_close_matches = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

_close_to_open_matches = {v: k for k, v in _open_to_close_matches.items()}


def mismatching_brackets(line: str) -> Iterator[chr]:
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            opening = stack.pop()
            if _open_to_close_matches[opening] != char:
                yield char


def missing_brackets(line: str) -> Iterator[chr]:
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            opening = stack.pop()
            if _open_to_close_matches[opening] != char:
                return
    while stack:
        yield _open_to_close_matches[stack.pop()]
