from utils import toBinary, toNumber
CHARS = 'fghijklmnopqrstu'


def cnvPairToBits(chars):
    chars = chars[:]
    a1 = CHARS.index(chars[0])
    b1 = toBinary(a1, 4)
    b1.reverse()
    a2 = CHARS.index(chars[1])
    b2 = toBinary(a2, 4)
    b2.reverse()
    bits = b1 + b2
    return bits


def cnvByteToPair(byte):
    byte = byte[:]
    b1 = byte[:4]
    b2 = byte[4:]
    b = [b1, b2]
    for bt in b:
        bt.reverse()
    n = [toNumber(bt) for bt in b]
    c = [CHARS[i] for i in n]
    return c[0] + c[1]


def toBits(text):
    text = text[:]
    if len(text) != 16:
        raise ValueError('Raw text should be of length 16')
    bytec = [text[i:i+2] for i in range(0, len(text), 2)]
    bytearr = [cnvPairToBits(bt) for bt in bytec]
    result = []
    for bt in bytearr:
        result += bt
    return result


def encode(text, padding=16):
    text = text[:]
    pdText = padText(text, padding)
    res = toBits(pdText)
    return res


def decode(block):
    block = block[:]
    bytearr = [block[i:i+8] for i in range(0, 64, 8)]
    pairs = [cnvByteToPair(bt) for bt in bytearr]
    res = ''
    for p in pairs:
        sr = p[0] + p[1]
        res += sr
    return res


def padText(text, length):
    if len(text) >= length:
        return text
    while len(text) < length:
        text += 'f'
    return text


def main():
    sr = 'ffffffff'
    # print(cnvPairToBits(['f', 't']))
    res = encode(sr)
    # d = decode(res)
    # print(res)
    # print(d)


if __name__ == '__main__':
    main()
