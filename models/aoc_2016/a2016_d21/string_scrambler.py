from typing import Protocol
from dataclasses import dataclass


class StringScrambler(Protocol):
    def scramble(self, s: str) -> str: ...

    def unscramble(self, s: str) -> str: ...


class MultiStepScrambler:
    def __init__(self, scramblers: list[StringScrambler]) -> None:
        self.scramblers = scramblers

    def scramble(self, s: str) -> str:
        for scrambler in self.scramblers:
            s = scrambler.scramble(s)
        return s

    def unscramble(self, s: str) -> str:
        for scrambler in reversed(self.scramblers):
            s = scrambler.unscramble(s)
        return s


@dataclass(frozen=True)
class LetterSwapScrambler:
    letter_a: chr
    letter_b: chr

    @staticmethod
    def swap_letters(s: str, x: chr, y: chr) -> str:
        return s.replace(x, "_").replace(y, x).replace("_", y)

    def scramble(self, s: str) -> str:
        return self.swap_letters(s, self.letter_a, self.letter_b)

    def unscramble(self, s: str) -> str:
        return self.scramble(s)


@dataclass(frozen=True)
class PositionSwapScrambler:
    position_a: int
    position_b: int

    def scramble(self, s: str) -> str:
        return LetterSwapScrambler.swap_letters(
            s, s[self.position_a], s[self.position_b]
        )

    def unscramble(self, s: str) -> str:
        return self.scramble(s)


@dataclass(frozen=True)
class RotationScrambler:
    steps: int

    @staticmethod
    def rotate_string(s: str, steps: int) -> str:
        cut = -steps % len(s)
        return s[cut:] + s[:cut]

    def scramble(self, s: str) -> str:
        return self.rotate_string(s, self.steps)

    def unscramble(self, s: str) -> str:
        return self.rotate_string(s, -self.steps)


@dataclass(frozen=True)
class LetterBasedRotationScrambler:
    letter: chr

    def scramble(self, s: str) -> str:
        letter_idx = s.index(self.letter)
        steps = 1 + letter_idx + (1 if letter_idx >= 4 else 0)
        return RotationScrambler.rotate_string(s, steps)

    def unscramble(self, s: str) -> str:
        if len(s) != 8:
            raise NotImplementedError("Cannot unscramble string of length != 8")
        letter_idx = s.index(self.letter)
        if letter_idx == 0:
            steps = -1
        elif letter_idx % 2 == 1:
            steps = -(letter_idx // 2) - 1
        else:
            steps = 3 - letter_idx // 2
        return RotationScrambler.rotate_string(s, steps)


@dataclass(frozen=True)
class ReversionScrambler:
    start: int
    end: int

    def scramble(self, s: str) -> str:
        return s[: self.start] + s[self.start : self.end + 1][::-1] + s[self.end + 1 :]

    def unscramble(self, s: str) -> str:
        return self.scramble(s)


@dataclass(frozen=True)
class LetterMoveScrambler:
    origin: int
    destination: int

    @staticmethod
    def move_letter(s: str, x: int, y: int) -> str:
        letter = s[x]
        s = s[:x] + s[x + 1 :]
        return s[:y] + letter + s[y:]

    def scramble(self, s: str) -> str:
        return self.move_letter(s, self.origin, self.destination)

    def unscramble(self, s: str) -> str:
        return self.move_letter(s, self.destination, self.origin)
