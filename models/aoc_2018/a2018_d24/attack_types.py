from enum import Enum


class AttackType(Enum):
    SLASHING = 1
    BLUDGEONING = 2
    RADIATION = 3
    FIRE = 4
    COLD = 5

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def from_str(s):
        if s == "slashing":
            return AttackType.SLASHING
        elif s == "bludgeoning":
            return AttackType.BLUDGEONING
        elif s == "radiation":
            return AttackType.RADIATION
        elif s == "fire":
            return AttackType.FIRE
        elif s == "cold":
            return AttackType.COLD
        else:
            raise ValueError(f"Unknown attack type: {s}")
