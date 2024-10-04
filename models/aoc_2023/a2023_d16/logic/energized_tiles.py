from .light_beam import LightBeam
from .mirror_contraption import MirrorContraption


def num_energized_tiles(initial_beam: LightBeam, contraption: MirrorContraption) -> int:
    visited = set()
    stack = {initial_beam}
    while stack:
        beam = stack.pop()
        if beam in visited:
            continue
        visited.add(beam)
        stack.update(contraption.propagate(beam))
    visited_positions = {beam.position for beam in visited}
    return len(visited_positions)
