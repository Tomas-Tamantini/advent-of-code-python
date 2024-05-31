from ..disc_system import SpinningDisc, DiscSystem


def test_if_single_disc_should_press_button_when_one_second_before_correct_position():
    single_disc = SpinningDisc(num_positions=19, position_at_time_zero=7)
    system = DiscSystem(discs=[single_disc])
    assert system.time_to_press_button() == 11


def test_if_multiple_discs_should_press_button_at_smallest_correct_time():
    discs = [
        SpinningDisc(num_positions=5, position_at_time_zero=4),
        SpinningDisc(num_positions=2, position_at_time_zero=1),
    ]
    system = DiscSystem(discs=discs)
    assert system.time_to_press_button() == 5


def test_can_add_more_discs_to_the_bottom_of_system():
    discs = [
        SpinningDisc(num_positions=5, position_at_time_zero=4),
        SpinningDisc(num_positions=2, position_at_time_zero=1),
    ]
    system = DiscSystem(discs=discs)
    system.add_disc(SpinningDisc(num_positions=3, position_at_time_zero=0))
    assert system.time_to_press_button() == 15
