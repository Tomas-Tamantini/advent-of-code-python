from typing import Iterator
from models.common.io import InputReader
from models.common.number_theory import Interval
from .logic import (
    Workflow,
    LessThanRule,
    GreaterThanRule,
    WorkflowRule,
    MachinePartRange,
)


def _parse_inequality_rule(rule_str: str) -> WorkflowRule:
    rule_parts = rule_str.split(":")
    next_workflow_id = rule_parts[-1].strip()
    inequality_sign = ">" if ">" in rule_parts[0] else "<"
    inequality_parts = rule_parts[0].split(inequality_sign)
    attribute_name = inequality_parts[0]
    threshold = int(inequality_parts[1])
    if inequality_sign == ">":
        return GreaterThanRule(attribute_name, threshold, next_workflow_id)
    else:
        return LessThanRule(attribute_name, threshold, next_workflow_id)


def _parse_workflow(line: str) -> Workflow:
    parts = line.split("{")
    workflow_id = parts[0]
    rules_repr = parts[1].replace("}", "").split(",")
    default_next_workflow_id = rules_repr.pop()
    rules = tuple(_parse_inequality_rule(rule) for rule in rules_repr)
    return Workflow(workflow_id, rules, default_next_workflow_id)


def parse_workflows(input_reader: InputReader) -> Iterator[Workflow]:
    for line in input_reader.read_stripped_lines():
        if line and line[0] != "{":
            yield _parse_workflow(line)


def _parse_machine_part_range(line: str) -> MachinePartRange:
    dict_repr = line.replace("{", "{'").replace("=", "':").replace(",", ",'")
    attribute_values = eval(dict_repr)
    attributes = {
        attribute_name: Interval(v, v) for attribute_name, v in attribute_values.items()
    }
    return MachinePartRange(attributes)


def parse_machine_part_ranges(input_reader: InputReader) -> Iterator[MachinePartRange]:
    for line in input_reader.read_stripped_lines():
        if line and line[0] == "{":
            yield _parse_machine_part_range(line)
