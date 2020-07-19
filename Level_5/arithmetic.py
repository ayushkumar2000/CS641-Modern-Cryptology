REDPOL = 0x83


def add(a, b):
    return a ^ b


def mul(a, b):
    p = 0
    while a and b:
        if b & 1:
            p ^= a
        if a & 0x40:
            a = (a << 1) ^ REDPOL
        else:
            a <<= 1
        b >>= 1
    return p


def exp(a, e):
    res = 1
    for i in range(e):
        res = mul(res, a)
    return res


def main():
    print(mul(42, 42))
    print(exp(42, 1))
    print(exp(42, 2))


if __name__ == '__main__':
    main()
