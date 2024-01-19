from typing import Protocol
from dataclasses import dataclass


class StringTransform(Protocol):
    def transform(self, string: str) -> str:
        ...


@dataclass
class Spin(StringTransform):
    num: int

    def transform(self, string: str) -> str:
        return string[-self.num :] + string[: -self.num]


@dataclass
class Exchange(StringTransform):
    pos_a: int
    pos_b: int

    def transform(self, string: str) -> str:
        chars = list(string)
        chars[self.pos_a], chars[self.pos_b] = chars[self.pos_b], chars[self.pos_a]
        return "".join(chars)


@dataclass
class Partner(StringTransform):
    name_a: str
    name_b: str

    def transform(self, string: str) -> str:
        return (
            string.replace(self.name_a, "X")
            .replace(self.name_b, self.name_a)
            .replace("X", self.name_b)
        )
