from models.aoc_2016 import MessageReconstructor


def test_message_is_reconstructed_by_the_most_common_character_in_each_position():
    messages = [
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar",
    ]

    reconstructor = MessageReconstructor(messages)

    assert reconstructor.reconstruct_message() == "easter"
