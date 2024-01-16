def sentence_contains_no_duplicates(sentence: str) -> bool:
    words = sentence.split()
    return len(words) == len(set(words))
