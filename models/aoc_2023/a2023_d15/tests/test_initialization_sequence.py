from ..logic import (
    HashCalculator,
    InsertLens,
    Lens,
    LensBox,
    RemoveLens,
    run_initialization_sequence,
)

"rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_running_initialization_sequence_runs_steps_in_order():
    boxes = [LensBox() for _ in range(4)]
    steps = [
        InsertLens(Lens("rn", 1)),
        RemoveLens("cm"),
        InsertLens(Lens("qp", 3)),
        InsertLens(Lens("cm", 2)),
        RemoveLens("qp"),
        InsertLens(Lens("pc", 4)),
        InsertLens(Lens("ot", 9)),
        InsertLens(Lens("ab", 5)),
        RemoveLens("pc"),
        InsertLens(Lens("pc", 6)),
        InsertLens(Lens("ot", 7)),
    ]
    run_initialization_sequence(boxes, steps, HashCalculator())
    assert list(boxes[0].lenses()) == [Lens("rn", 1), Lens("cm", 2)]
    assert list(boxes[1].lenses()) == []
    assert list(boxes[2].lenses()) == []
    assert list(boxes[3].lenses()) == [Lens("ot", 7), Lens("ab", 5), Lens("pc", 6)]
