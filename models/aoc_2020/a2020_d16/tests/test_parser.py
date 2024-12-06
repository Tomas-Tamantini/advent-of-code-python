from models.common.io import InputFromString
from models.common.number_theory import Interval

from ..parser import parse_ticket_validator_and_ticket_values
from ..ticket_validator import TicketFieldValidator, TicketValidator


def test_parse_ticket_validator_and_ticket_values():
    file_content = """
                   class: 1-3 or 5-7
                   row: 6-11 or 33-44
                   seat: 13-40 or 45-50

                   your ticket:
                   7,1,14

                   nearby tickets:
                   7,3,47
                   40,4,50
                   55,2,20
                   38,6,12
                   """
    parsed = parse_ticket_validator_and_ticket_values(InputFromString(file_content))
    assert parsed.my_ticket == (7, 1, 14)
    assert parsed.nearby_tickets == [
        (7, 3, 47),
        (40, 4, 50),
        (55, 2, 20),
        (38, 6, 12),
    ]
    assert parsed.validator == TicketValidator(
        field_validators=(
            TicketFieldValidator(
                field_name="class", intervals=(Interval(1, 3), Interval(5, 7))
            ),
            TicketFieldValidator(
                field_name="row", intervals=(Interval(6, 11), Interval(33, 44))
            ),
            TicketFieldValidator(
                field_name="seat", intervals=(Interval(13, 40), Interval(45, 50))
            ),
        )
    )
