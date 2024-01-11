from dataclasses import dataclass


@dataclass(frozen=True)
class EncryptedRoom:
    room_name: str
    sector_id: int
    checksum: str

    def _letter_counts(self) -> dict[str, int]:
        letter_counts = {}
        for letter in self.room_name:
            if letter != "-":
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
        return letter_counts

    def _proper_checksum(self) -> str:
        return "".join(
            letter
            for letter, _ in sorted(
                self._letter_counts().items(), key=lambda item: (-item[1], item[0])
            )
        )[:5]

    def is_real(self) -> bool:
        return self.checksum == self._proper_checksum()
