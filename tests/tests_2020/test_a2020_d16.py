from models.aoc_2020 import RangeInterval, TicketFieldValidator, TicketValidator


def test_range_interval_contains_numbers_within_it_including_endpoints():
    interval = RangeInterval(1, 3)
    assert interval.contains(1)
    assert interval.contains(2)
    assert interval.contains(3)
    assert not interval.contains(0)
    assert not interval.contains(4)
    assert not interval.contains(5)


def test_ticket_field_is_invalid_if_it_is_not_contained_in_any_interval_of_given_validator():
    field_validator = TicketFieldValidator(
        field_name="row",
        intervals=(RangeInterval(1, 3), RangeInterval(5, 7)),
    )
    assert not field_validator.is_valid(0)
    assert not field_validator.is_valid(4)
    assert not field_validator.is_valid(8)


def test_ticket_field_is_valid_if_it_is_contained_in_any_interval_of_given_validator():
    field_validator = TicketFieldValidator(
        field_name="row",
        intervals=(RangeInterval(1, 3), RangeInterval(5, 7)),
    )
    assert field_validator.is_valid(1)
    assert field_validator.is_valid(2)
    assert field_validator.is_valid(3)
    assert field_validator.is_valid(5)
    assert field_validator.is_valid(6)
    assert field_validator.is_valid(7)


def test_ticket_field_is_invalid_if_it_is_not_validated_by_any_validator():
    field_a_validator = TicketFieldValidator(
        field_name="row",
        intervals=(RangeInterval(1, 3), RangeInterval(5, 7)),
    )
    field_b_validator = TicketFieldValidator(
        field_name="seat", intervals=(RangeInterval(10, 20),)
    )
    ticket_validator = TicketValidator(
        field_validators=(field_a_validator, field_b_validator)
    )
    assert not ticket_validator.is_valid_field(0)


def test_ticket_field_is_valid_if_it_is_validated_by_any_validator():
    field_a_validator = TicketFieldValidator(
        field_name="row",
        intervals=(RangeInterval(1, 3), RangeInterval(5, 7)),
    )
    field_b_validator = TicketFieldValidator(
        field_name="seat", intervals=(RangeInterval(10, 20),)
    )
    ticket_validator = TicketValidator(
        field_validators=(field_a_validator, field_b_validator)
    )
    assert ticket_validator.is_valid_field(15)
