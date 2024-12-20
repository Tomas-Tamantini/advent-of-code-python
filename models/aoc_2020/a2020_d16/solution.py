from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_ticket_validator_and_ticket_values


def aoc_2020_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 16, "Ticket Translation")
    io_handler.output_writer.write_header(problem_id)
    parsed_ticket_validator = parse_ticket_validator_and_ticket_values(
        io_handler.input_reader
    )
    validator = parsed_ticket_validator.validator
    nearby_tickets = parsed_ticket_validator.nearby_tickets
    scanning_error_rate = sum(
        value
        for ticket in nearby_tickets
        for value in ticket
        if not validator.is_valid_field(value)
    )
    yield ProblemSolution(
        problem_id,
        f"The scanning error rate is {scanning_error_rate}",
        part=1,
        result=scanning_error_rate,
    )

    my_ticket = parsed_ticket_validator.my_ticket
    fields_to_positions = validator.map_fields_to_positions(
        [my_ticket] + nearby_tickets
    )
    product = 1
    for field_name, position in fields_to_positions.items():
        if field_name.startswith("departure"):
            product *= my_ticket[position]
    yield ProblemSolution(
        problem_id,
        f"Product of 'departure' fields on my ticket is {product}",
        part=2,
        result=product,
    )
