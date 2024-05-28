from .frequency_transmission import flawed_frequency_transmission


def test_applying_fft_zero_times_returns_same_list():
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    assert flawed_frequency_transmission(signal, num_phases=0) == signal


def test_applying_fft_one_time_returns_list_modified_by_repeating_patterns():
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    num_phases = 1
    assert flawed_frequency_transmission(signal, num_phases) == [4, 8, 2, 2, 6, 1, 5, 8]


def test_fft_can_be_applied_multiple_times():
    signal = [1, 2, 3, 4, 5, 6, 7, 8]
    num_phases = 4
    assert flawed_frequency_transmission(signal, num_phases) == [0, 1, 0, 2, 9, 4, 9, 8]
