def sentence_contains_no_duplicates(sentence: str) -> bool:
    words = sentence.split()
    return len(words) == len(set(words))


def sentence_contains_no_anagrams(sentence: str) -> bool:
    words = sentence.split()
    sorted_words = ["".join(sorted(word)) for word in words]
    return len(sorted_words) == len(set(sorted_words))
