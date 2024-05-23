from models.common.io import InputFromString
from ..parser import parse_crates
from ..logic import MoveCrateItems


def test_parse_crates():
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
    parsed_crates = parse_crates(input_reader)
    assert len(parsed_crates.crates) == 3
    assert parsed_crates.crates[1].peek() == "N"
    assert parsed_crates.crates[2].peek() == "D"
    assert parsed_crates.crates[3].peek() == "P"
    assert parsed_crates.moves == [
        MoveCrateItems(num_times=1, origin_id=2, destination_id=1),
        MoveCrateItems(num_times=4, origin_id=1, destination_id=3),
    ]
