import pytest

from models.common.io import InputFromString

from ..logic import MoveCratesMultipleAtATime, MoveCratesOneAtATime
from ..parser import parse_crates


@pytest.mark.parametrize(
    "move_one_at_a_time, move_cls",
    [(True, MoveCratesOneAtATime), (False, MoveCratesMultipleAtATime)],
)
def test_parse_crates(move_one_at_a_time, move_cls):
    input_reader = InputFromString(
        """
            [D]    
        [N] [C]    
        [Z] [M] [P]
         1   2   3 

        move 1 from 2 to 1
        move 4 from 1 to 3
        """
    )
    parsed_crates = parse_crates(input_reader, move_one_at_a_time)
    assert len(parsed_crates.crates) == 3
    assert parsed_crates.crates[1].peek() == "N"
    assert parsed_crates.crates[2].peek() == "D"
    assert parsed_crates.crates[3].peek() == "P"
    assert parsed_crates.moves == [
        move_cls(num_times=1, origin_id=2, destination_id=1),
        move_cls(num_times=4, origin_id=1, destination_id=3),
    ]
