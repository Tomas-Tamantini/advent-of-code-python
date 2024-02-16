from .intcode import IntcodeProgram, run_intcode_program


def run_intcode_program_until_halt(sequence: list[int]) -> list[int]:
    program = IntcodeProgram(sequence[:])
    run_intcode_program(program)
    return program.sequence


def noun_and_verb_for_given_output(
    sequence: list[int],
    desired_output: int,
    noun_range: int = 100,
    verb_range: int = 100,
) -> tuple[int, int]:
    for verb in range(noun_range):
        for noun in range(verb_range):
            copied_seq = sequence[:]
            copied_seq[1] = noun
            copied_seq[2] = verb
            try:
                final_state = run_intcode_program_until_halt(copied_seq)
            except IndexError:
                continue
            if final_state[0] == desired_output:
                return noun, verb
    raise ValueError("No noun and verb found for the given output")
