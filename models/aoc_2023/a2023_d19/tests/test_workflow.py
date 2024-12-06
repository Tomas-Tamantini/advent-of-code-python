from models.common.number_theory import Interval

from ..logic import (
    GreaterThanRule,
    LessThanRule,
    MachinePartRange,
    MachinePartState,
    Workflow,
    WorkflowNetwork,
)


def _default_part_ranges() -> MachinePartRange:
    return MachinePartRange(
        {
            "x": Interval(1, 10),
            "m": Interval(1, 10),
            "a": Interval(1, 10),
            "s": Interval(1, 10),
        }
    )


def test_number_of_parts_in_machine_part_range_is_product_of_number_of_parts_in_each_attribute():
    part_range = MachinePartRange(
        {
            "x": Interval(1, 3),
            "m": Interval(11, 12),
            "a": Interval(15, 15),
            "s": Interval(1001, 1005),
        }
    )
    assert part_range.num_parts() == 30


def test_less_than_rule_splits_range_into_match_and_non_match_ranges():
    input_range = _default_part_ranges()
    rule = LessThanRule(
        attribute_name="m", threshold=5, next_workflow_id="next_workflow"
    )
    split_range = rule.split_range(input_range)
    assert split_range.match_range == MachinePartRange(
        {
            "x": Interval(1, 10),
            "m": Interval(1, 4),
            "a": Interval(1, 10),
            "s": Interval(1, 10),
        }
    )
    assert split_range.non_match_range == MachinePartRange(
        {
            "x": Interval(1, 10),
            "m": Interval(5, 10),
            "a": Interval(1, 10),
            "s": Interval(1, 10),
        }
    )


def test_greater_than_rule_splits_range_into_match_and_non_match_ranges():
    input_range = _default_part_ranges()
    rule = GreaterThanRule(
        attribute_name="x", threshold=3, next_workflow_id="next_workflow"
    )
    split_range = rule.split_range(input_range)
    assert split_range.match_range == MachinePartRange(
        {
            "x": Interval(4, 10),
            "m": Interval(1, 10),
            "a": Interval(1, 10),
            "s": Interval(1, 10),
        }
    )
    assert split_range.non_match_range == MachinePartRange(
        {
            "x": Interval(1, 3),
            "m": Interval(1, 10),
            "a": Interval(1, 10),
            "s": Interval(1, 10),
        }
    )


def test_workflow_splits_machine_part_ranges_into_subranges_in_order_of_rule():
    input_range = _default_part_ranges()
    workflow = Workflow(
        workflow_id="test_workflow",
        rules=(
            LessThanRule(
                attribute_name="m",
                threshold=3,
                next_workflow_id="m_less_than_3",
            ),
            LessThanRule(
                attribute_name="m",
                threshold=2,
                next_workflow_id="m_less_than_2",
            ),
            GreaterThanRule(
                attribute_name="s",
                threshold=7,
                next_workflow_id="s_greater_than_7",
            ),
            GreaterThanRule(
                attribute_name="x",
                threshold=1,
                next_workflow_id="x_greater_than_one",
            ),
        ),
        default_next_workflow_id="default",
    )
    next_states = list(workflow.next_part_states(input_range))
    assert next_states == [
        MachinePartState(
            workflow_id="m_less_than_3",
            part_range=MachinePartRange(
                {
                    "x": Interval(1, 10),
                    "m": Interval(1, 2),
                    "a": Interval(1, 10),
                    "s": Interval(1, 10),
                }
            ),
        ),
        MachinePartState(
            workflow_id="s_greater_than_7",
            part_range=MachinePartRange(
                {
                    "x": Interval(1, 10),
                    "m": Interval(3, 10),
                    "a": Interval(1, 10),
                    "s": Interval(8, 10),
                }
            ),
        ),
        MachinePartState(
            workflow_id="x_greater_than_one",
            part_range=MachinePartRange(
                {
                    "x": Interval(2, 10),
                    "m": Interval(3, 10),
                    "a": Interval(1, 10),
                    "s": Interval(1, 7),
                }
            ),
        ),
        MachinePartState(
            workflow_id="default",
            part_range=MachinePartRange(
                {
                    "x": Interval(1, 1),
                    "m": Interval(3, 10),
                    "a": Interval(1, 10),
                    "s": Interval(1, 7),
                }
            ),
        ),
    ]


def test_workflow_network_yields_accepted_ranges():
    network = WorkflowNetwork(
        initial_workflow_id="in",
        accept_workflow_id="A",
        reject_workflow_id="R",
        workflows=(
            Workflow(
                workflow_id="in",
                rules=(
                    LessThanRule("m", 3, "m_less_than_3"),
                    GreaterThanRule("s", 7, "R"),
                ),
                default_next_workflow_id="A",
            ),
            Workflow(
                workflow_id="m_less_than_3",
                rules=(
                    LessThanRule("x", 6, "A"),
                    GreaterThanRule("a", 2, "A"),
                ),
                default_next_workflow_id="R",
            ),
        ),
    )
    initial_range = _default_part_ranges()
    accepted_ranges = tuple(network.accepted_ranges(initial_range))
    assert accepted_ranges == (
        MachinePartRange(
            {
                "x": Interval(min_inclusive=1, max_inclusive=10),
                "m": Interval(min_inclusive=3, max_inclusive=10),
                "a": Interval(min_inclusive=1, max_inclusive=10),
                "s": Interval(min_inclusive=1, max_inclusive=7),
            }
        ),
        MachinePartRange(
            {
                "x": Interval(min_inclusive=6, max_inclusive=10),
                "m": Interval(min_inclusive=1, max_inclusive=2),
                "a": Interval(min_inclusive=3, max_inclusive=10),
                "s": Interval(min_inclusive=1, max_inclusive=10),
            }
        ),
        MachinePartRange(
            {
                "x": Interval(min_inclusive=1, max_inclusive=5),
                "m": Interval(min_inclusive=1, max_inclusive=2),
                "a": Interval(min_inclusive=1, max_inclusive=10),
                "s": Interval(min_inclusive=1, max_inclusive=10),
            }
        ),
    )
