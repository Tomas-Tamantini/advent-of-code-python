from .packet_arrangement import possible_arrangements_of_packets_in_passenger_comparment


def test_can_find_smallest_number_of_packets_to_go_in_passenger_compartment():
    numbers = (1, 2, 3, 4, 5, 7, 8, 9, 10, 11)
    num_groups = 3

    arrangements = tuple(
        possible_arrangements_of_packets_in_passenger_comparment(numbers, num_groups)
    )

    assert len(arrangements) == 1
    assert arrangements[0] == (11, 9)


def test_ensures_that_packets_can_be_evenly_balanced():
    numbers = (1, 5, 9)
    num_groups = 3

    arrangements = tuple(
        possible_arrangements_of_packets_in_passenger_comparment(numbers, num_groups)
    )

    assert len(arrangements) == 0
