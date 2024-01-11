from typing import Iterator


class IpParser:
    def __init__(self, ip: str) -> None:
        self._ip = ip
        self._supernet_sequences = []
        self._hypernet_sequences = []
        self._parse()

    def _ip_components(self) -> Iterator[tuple[str, bool]]:
        current_sequence = ""
        for c in self._ip:
            if c == "[":
                yield current_sequence, False
                current_sequence = ""
            elif c == "]":
                yield current_sequence, True
                current_sequence = ""
            else:
                current_sequence += c
        if current_sequence:
            yield current_sequence, False

    def _parse(self) -> None:
        for sequence, is_inside_bracket in self._ip_components():
            if is_inside_bracket:
                self._hypernet_sequences.append(sequence)
            else:
                self._supernet_sequences.append(sequence)

    @staticmethod
    def _contains_abba(text: str) -> bool:
        for i in range(len(text) - 3):
            if (
                text[i] == text[i + 3]
                and text[i + 1] == text[i + 2]
                and text[i] != text[i + 1]
            ):
                return True
        return False

    @staticmethod
    def _aba_sequences(text: str) -> Iterator[str]:
        for i in range(len(text) - 2):
            if text[i] == text[i + 2] and text[i] != text[i + 1]:
                yield text[i : i + 3]

    @staticmethod
    def _invert_aba_sequence(aba: str) -> str:
        return aba[1] + aba[0] + aba[1]

    def supports_tls(self) -> bool:
        for sequence in self._hypernet_sequences:
            if self._contains_abba(sequence):
                return False
        for sequence in self._supernet_sequences:
            if self._contains_abba(sequence):
                return True
        return False

    def supports_ssl(self) -> bool:
        supernet_aba_sequences = {
            aba
            for sequence in self._supernet_sequences
            for aba in self._aba_sequences(sequence)
        }
        hypernet_aba_sequences = {
            aba
            for sequence in self._hypernet_sequences
            for aba in self._aba_sequences(sequence)
        }
        inverted_hypernet_sequences = {
            self._invert_aba_sequence(aba) for aba in hypernet_aba_sequences
        }
        return bool(supernet_aba_sequences & inverted_hypernet_sequences)
