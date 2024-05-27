from typing import Iterator

_open_to_close_matches = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


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
