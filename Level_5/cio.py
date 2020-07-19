ALPHABET = 'fghijklmnopqrstu'


def _byteToChar(bytec):
    byte = bytec[:]
    byte.reverse()
    n = 0
    for i in range(8):
        n += byte[i]*(2**i)
    return str(chr(n))


def _to4Bit(char):
    n = ALPHABET.index(char)
    bi = []
    for i in range(4):
        r = n % 2
        n = n//2
        bi.append(r)
    bi.reverse()
    return bi


def _toBlock(chars):
    idxs = [ALPHABET.index(char) for char in chars]
    block = idxs[0]*16 + idxs[1]
    if block > 127:
        raise ValueError(
            f"Block value cannot be greater than 127. Found in chars '{chars}'")
    return block


def _toChars(block):
    if block > 127:
        raise ValueError(f"Block value cannot be greater than 127.")
    n1, n2 = block//16, block % 16
    char1, char2 = ALPHABET[n1], ALPHABET[n2]
    return char1 + char2


def _padWith(stri, elem, length):
    while len(stri) < length:
        stri += elem
    return stri


def encode(text):
    if len(text) != 8:
        raise ValueError("Length of blocktext must be 8 blocks.")
    res = ''
    for block in text:
        ch = _toChars(block)
        res += ch
    return res


def decode(text):
    if len(text) != 16:
        raise ValueError("Length of alphatext must be 16 chars.")
    res = []
    for i in range(0, 16, 2):
        block = _toBlock(text[i:i+2])
        res.append(block)
    return res


def finalDecode(text):
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    ans = ''
    for pair in pairs:
        bis = [_to4Bit(c) for c in pair]
        total = bis[0] + bis[1]
        c = _byteToChar(total)
        ans += c
    return ans


def main():
    # comp1 = [117, 118, 113, 114, 105, 105, 111, 104]
    # comp2 = [118, 111, 101, 121, 106, 102, 122, 114]
    # p1 = encode(comp1)
    # p2 = encode(comp2)
    # p = p1 + p2
    ans = finalDecode('mkmlmgmhlololulnmllulkmolpllmpmh')
    print(ans)


if __name__ == '__main__':
    main()
