def gcd(*n: int) -> int:
    if len(n) == 1:
        return n[0]
    if len(n) == 2:
        a, b = n
        if b == 0:
            return a
        return gcd(b, a % b)
    return gcd(n[0], gcd(*n[1:]))


def lcm(*n: int) -> int:
    if any(x == 0 for x in n):
        return 0
    if len(n) == 1:
        return n[0]
    if len(n) == 2:
        a, b = n
        return a * b // gcd(a, b)
    return lcm(n[0], lcm(*n[1:]))


def are_coprime(*n: int) -> bool:
    return gcd(*n) == 1
