def _fuel_for_mass(mass: int) -> int:
    return max(0, mass // 3 - 2)


def fuel_requirement(rocket_mass: int, consider_fuel_mass: bool) -> int:
    fuel = _fuel_for_mass(rocket_mass)
    if not consider_fuel_mass:
        return fuel
    extra_mass = fuel
    while extra_mass:
        extra_mass = _fuel_for_mass(extra_mass)
        fuel += extra_mass
    return fuel
