from dataclasses import dataclass

from models.common.io import InputReader
from models.common.number_theory import Interval

from .ticket_validator import TicketFieldValidator, TicketValidator


@dataclass
class _ParsedTicketValidator:
    validator: TicketValidator
    my_ticket: tuple[int]
    nearby_tickets: list[tuple[int]]


def _parse_ticket_field_validator(line: str) -> TicketFieldValidator:
    parts = line.split(": ")
    field_name = parts[0]
    ranges = []
    for part in parts[1].split(" or "):
        min_value, max_value = map(int, part.split("-"))
        ranges.append(Interval(min_value, max_value))
    return TicketFieldValidator(field_name, tuple(ranges))


def parse_ticket_validator_and_ticket_values(
    input_reader: InputReader,
) -> _ParsedTicketValidator:
    document_section = 0
    field_validators = []
    my_ticket = None
    nearby_tickets = []

    lines = list(input_reader.readlines())

    for line in lines:
        if not line.strip():
            continue
        if "your ticket" in line:
            document_section += 1
        elif "nearby tickets" in line:
            document_section += 1
        elif document_section == 0:
            field_validators.append(_parse_ticket_field_validator(line.strip()))
        elif document_section == 1:
            my_ticket = tuple(map(int, line.strip().split(",")))
        elif document_section == 2:
            nearby_tickets.append(tuple(map(int, line.strip().split(","))))
        else:
            raise ValueError(f"Unknown document section: {document_section}")

    return _ParsedTicketValidator(
        TicketValidator(tuple(field_validators)), my_ticket, nearby_tickets
    )
