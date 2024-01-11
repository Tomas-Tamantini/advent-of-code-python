from models.aoc_2016 import MessageReconstructor

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


def test_message_can_be_reconstructed_by_the_most_common_character_in_each_position():
    reconstructor = MessageReconstructor(messages)
    assert reconstructor.reconstruct_message_from_most_common_chars() == "easter"


def test_message_can_be_reconstructed_by_the_least_common_character_in_each_position():
    reconstructor = MessageReconstructor(messages)
    assert reconstructor.reconstruct_message_from_least_common_chars() == "advent"
