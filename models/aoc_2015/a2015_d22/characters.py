from dataclasses import dataclass


@dataclass(frozen=True)
class Boss:
    hit_points: int

    def is_dead(self):
        return self.hit_points <= 0

    def take_damage(self, damage) -> "Boss":
        return Boss(self.hit_points - damage)


@dataclass(frozen=True)
class Wizard:
    hit_points: int
    mana: int
    armor: int = 0

    def is_dead(self):
        return self.hit_points <= 0

    def take_damage(self, damage) -> "Wizard":
        damage = max(1, damage - self.armor)
        return Wizard(self.hit_points - damage, self.mana, self.armor)

    def heal(self, heal: int) -> "Wizard":
        return Wizard(self.hit_points + heal, self.mana, self.armor)

    def spend_mana(self, mana_cost: int) -> "Wizard":
        return Wizard(self.hit_points, self.mana - mana_cost, self.armor)

    def recharge_mana(self, mana: int) -> "Wizard":
        return Wizard(self.hit_points, self.mana + mana, self.armor)

    def add_armor(self, armor: int) -> "Wizard":
        return Wizard(self.hit_points, self.mana, armor)

    def remove_armor(self) -> "Wizard":
        return Wizard(self.hit_points, self.mana, 0)


@dataclass(frozen=True)
class CharactersState:
    wizard: Wizard
    boss: Boss
