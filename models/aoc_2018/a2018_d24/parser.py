from models.common.io import InputReader
from .logic import ArmyGroup, AttackType, InfectionGameState


def _parse_army_group(group_id: int, line: str) -> ArmyGroup:
    line = line.strip()
    units = int(line.split(" ")[0])
    hit_points = int(line.split(" ")[4])
    initiative = int(line.split(" ")[-1])
    attack_damage = int(line.split(" ")[-6])
    attack_type = AttackType.from_str(line.split(" ")[-5])
    weaknesses = []
    immunities = []
    if "(" in line:
        within_parentheses = line.split("(")[-1].split(")")[0]
        for part in within_parentheses.split(";"):
            if "weak" in part:
                weaknesses = [
                    AttackType.from_str(p.strip())
                    for p in part.replace("weak to", "").split(",")
                ]
            else:
                immunities = [
                    AttackType.from_str(p.strip())
                    for p in part.replace("immune to", "").split(",")
                ]

    return ArmyGroup(
        group_id=group_id,
        num_units=units,
        hit_points_per_unit=hit_points,
        attack_damage_per_unit=attack_damage,
        initiative=initiative,
        attack_type=attack_type,
        weaknesses=tuple(weaknesses),
        immunities=tuple(immunities),
    )


def parse_infection_game(input_reader: InputReader) -> InfectionGameState:
    immune_system_armies = []
    infection_armies = []
    loading_immune_system = True
    group_id = 1
    for line in input_reader.readlines():
        if "Infection" in line:
            loading_immune_system = False
        elif "Immune" in line:
            loading_immune_system = True
        elif "units" in line:
            army_group = _parse_army_group(group_id, line)
            group_id += 1
            if loading_immune_system:
                immune_system_armies.append(army_group)
            else:
                infection_armies.append(army_group)
    return InfectionGameState(
        immune_system_armies=tuple(immune_system_armies),
        infection_armies=tuple(infection_armies),
    )
