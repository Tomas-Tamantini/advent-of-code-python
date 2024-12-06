from models.common.io import InputReader

from .card_shuffle import (
    CutCardsShuffle,
    DealIntoNewStackShuffle,
    DealWithIncrementShuffle,
    MultiTechniqueShuffle,
)


def parse_multi_technique_shuffle(input_reader: InputReader) -> MultiTechniqueShuffle:
    techniques = []
    for line in input_reader.readlines():
        if "deal into new stack" in line:
            techniques.append(DealIntoNewStackShuffle())
        elif "cut" in line:
            techniques.append(CutCardsShuffle(int(line.split()[-1])))
        elif "deal with increment" in line:
            techniques.append(DealWithIncrementShuffle(int(line.split()[-1])))
    return MultiTechniqueShuffle(techniques)
