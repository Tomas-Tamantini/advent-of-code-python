class HashCalculator:
    @staticmethod
    def get_hash(text: str) -> int:
        total = 0
        for character in text:
            total += ord(character)
            total = (total * 17) % 256
        return total
