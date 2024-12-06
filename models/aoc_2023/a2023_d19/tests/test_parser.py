from models.common.io import InputFromString
from models.common.number_theory import Interval

from ..logic import MachinePartRange, MachinePartState
from ..parser import parse_machine_part_ranges, parse_workflows

_FILE_CONTENT = """
px{a<2006:qkq,m>2090:A,rfg}
lnx{m>1548:A,A}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
"""


def test_parse_workflows():
    input_reader = InputFromString(_FILE_CONTENT)
    workflows = list(parse_workflows(input_reader))
    assert [w.workflow_id for w in workflows] == ["px", "lnx"]
    test_range = MachinePartRange({"a": Interval(1, 5000), "m": Interval(1, 5000)})
    next_states = list(workflows[0].next_part_states(test_range))
    assert next_states == [
        MachinePartState(
            "qkq", MachinePartRange({"a": Interval(1, 2005), "m": Interval(1, 5000)})
        ),
        MachinePartState(
            "A",
            MachinePartRange({"a": Interval(2006, 5000), "m": Interval(2091, 5000)}),
        ),
        MachinePartState(
            "rfg", MachinePartRange({"a": Interval(2006, 5000), "m": Interval(1, 2090)})
        ),
    ]


def test_parse_machine_part_range():
    input_reader = InputFromString(_FILE_CONTENT)
    ranges = list(parse_machine_part_ranges(input_reader))
    assert ranges == [
        MachinePartRange(
            {
                "x": Interval(787, 787),
                "m": Interval(2655, 2655),
                "a": Interval(1222, 1222),
                "s": Interval(2876, 2876),
            }
        ),
        MachinePartRange(
            {
                "x": Interval(1679, 1679),
                "m": Interval(44, 44),
                "a": Interval(2067, 2067),
                "s": Interval(496, 496),
            }
        ),
        MachinePartRange(
            {
                "x": Interval(2036, 2036),
                "m": Interval(264, 264),
                "a": Interval(79, 79),
                "s": Interval(2244, 2244),
            }
        ),
    ]
