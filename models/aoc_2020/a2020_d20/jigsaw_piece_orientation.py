from dataclasses import dataclass


@dataclass(frozen=True)
class JigsawPieceOrientation:
    num_quarter_turns: int
    is_flipped: bool

    @staticmethod
    def all_possible_orientations():
        for num_quarter_turns in range(4):
            for is_flipped in (False, True):
                yield JigsawPieceOrientation(num_quarter_turns, is_flipped)
