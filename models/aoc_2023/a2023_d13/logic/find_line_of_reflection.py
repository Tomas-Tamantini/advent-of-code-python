from .ash_valley import AshValley
from .line_of_reflection import (
    LineOfReflection,
    HorizontalLineOfReflection,
    VerticalLineOfReflection,
)


def _is_symmetric_about_line(
    line_of_reflection: LineOfReflection, valley: AshValley, num_mismatches: int
):
    total_mismatches = 0
    for pos_a, pos_b in line_of_reflection.mirror_positions(valley):
        if valley.get_tile(pos_a) != valley.get_tile(pos_b):
            total_mismatches += 1
            if total_mismatches > num_mismatches:
                return False
    return total_mismatches == num_mismatches


def find_line_of_reflection(valley: AshValley, num_mismatches: int) -> LineOfReflection:
    for lor_cls in (HorizontalLineOfReflection, VerticalLineOfReflection):
        dimension = lor_cls.dimension(valley)
        for line_index in range(dimension - 1):
            line_of_reflection = lor_cls(line_index)
            if _is_symmetric_about_line(line_of_reflection, valley, num_mismatches):
                return line_of_reflection
