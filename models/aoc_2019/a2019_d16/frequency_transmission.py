import numpy as np


def flawed_frequency_transmission(
    signal: list[int],
    num_phases: int,
    offset: int = 0,
    num_elements_result: int = 8,
) -> list[int]:
    num_elements = len(signal)
    if offset > num_elements // 2:
        return _fast_flawed_frequency_transmission(
            signal, num_phases, offset, num_elements_result
        )
    else:
        return _slow_flawed_frequency_transmission(
            signal, num_phases, offset, num_elements_result
        )


def _slow_flawed_frequency_transmission(
    signal: list[int],
    num_phases: int,
    offset: int = 0,
    num_elements_result: int = 8,
) -> list[int]:
    num_elements = len(signal)
    for _ in range(num_phases):
        new_signal = []
        for i in range(num_elements):
            pattern = [0, 1, 0, -1]
            pattern = np.repeat(pattern, i + 1)
            pattern = np.tile(pattern, int(np.ceil((num_elements + 1) / len(pattern))))
            pattern = pattern[1 : num_elements + 1]
            new_signal.append(abs(np.dot(signal, pattern)) % 10)
        signal = new_signal
    return signal[offset : offset + num_elements_result]


def _fast_flawed_frequency_transmission(
    signal: list[int],
    num_phases: int,
    offset: int = 0,
    num_elements_result: int = 8,
) -> list[int]:
    signal = signal[offset:]
    results = signal[0:num_elements_result]
    next_top = num_phases
    next_bottom = 1
    thing_acc = 1
    for n in range(1, len(signal)):
        thing_acc = thing_acc * next_top // next_bottom
        next_top += 1
        next_bottom += 1
        for i in range(num_elements_result):
            if n + i >= len(signal):
                continue
            results[i] = (results[i] + thing_acc * signal[n + i]) % 10
    return results
