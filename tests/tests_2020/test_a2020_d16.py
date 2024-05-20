from models.common.number_theory import Interval
from models.aoc_2020 import TicketFieldValidator, TicketValidator


def test_ticket_field_is_invalid_if_it_is_not_contained_in_any_interval_of_given_validator():
    field_validator = TicketFieldValidator(
        field_name="row",
        intervals=(Interval(1, 3), Interval(5, 7)),
    )
    assert not field_validator.is_valid(0)
    assert not field_validator.is_valid(4)
    assert not field_validator.is_valid(8)


def test_ticket_field_is_valid_if_it_is_contained_in_any_interval_of_given_validator():
    field_validator = TicketFieldValidator(
        field_name="row",
        intervals=(Interval(1, 3), Interval(5, 7)),
    )
    assert field_validator.is_valid(1)
    assert field_validator.is_valid(2)
    assert field_validator.is_valid(3)
    assert field_validator.is_valid(5)
    assert field_validator.is_valid(6)
    assert field_validator.is_valid(7)


ticket_validator = TicketValidator(
    field_validators=(
        TicketFieldValidator(
            field_name="row",
            intervals=(Interval(1, 3), Interval(5, 7)),
        ),
        TicketFieldValidator(
            field_name="seat",
            intervals=(Interval(10, 20),),
        ),
    )
)


def test_ticket_field_is_invalid_if_it_is_not_validated_by_any_validator():
    assert not ticket_validator.is_valid_field(0)


def test_ticket_field_is_valid_if_it_is_validated_by_any_validator():
    assert ticket_validator.is_valid_field(15)


def test_ticket_is_not_valid_if_some_of_its_fields_is_invalid():
    ticket = (1, 100)
    assert not ticket_validator.is_valid_ticket(ticket)


def test_ticket_is_valid_if_all_of_its_fields_is_valid():
    ticket = (15, 1)
    assert ticket_validator.is_valid_ticket(ticket)


def test_ticket_validator_can_deduce_and_map_fields_to_positions_given_enough_tickets_ignoring_invalid_tickets():
    validator = TicketValidator(
        field_validators=(
            TicketFieldValidator(
                field_name="class",
                intervals=(Interval(0, 1), Interval(4, 19)),
            ),
            TicketFieldValidator(
                field_name="row",
                intervals=(Interval(0, 5), Interval(8, 19)),
            ),
            TicketFieldValidator(
                field_name="seat",
                intervals=(Interval(0, 13), Interval(16, 19)),
            ),
        )
    )

    tickets = [
        (11, 12, 13),
        (3, 9, 18),
        (15, 1, 5),
        (1000, 2000, 3000),  # Invalid ticket
        (5, 14, 9),
    ]

    assert validator.map_fields_to_positions(tickets) == {
        "class": 1,
        "row": 0,
        "seat": 2,
    }
