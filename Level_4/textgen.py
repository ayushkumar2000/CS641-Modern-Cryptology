from utils import applyPerm, toBinary
from constants import ip
from cio import encode, decode

IP_INVERSE = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21,
              61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

IPINV_INVERSE = [57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23,
                 15, 7, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8]


def getPlaintext(text):
    # text = encode(text)
    text = text[:]
    if len(text) != 64:
        raise ValueError("Desired binary plaintext must be 64 bits long")
    res = applyPerm(text, IP_INVERSE, 64)
    # print(res)
    res = decode(res)
    return res


def getCiphertext(textc):
    text = textc[:]
    d = encode(text)
    if len(d) != 64:
        raise ValueError("Length of encoded should be 64")
    res = applyPerm(d, IPINV_INVERSE, 64)
    return res


def generatePair(l):
    l = l[:]
    l1 = l[0]
    l2 = l[1]
    c1 = encode(l1)
    c2 = encode(l2)
    # print(c1)
    p1 = getPlaintext(c1)
    p2 = getPlaintext(c2)
    return [p1, p2]


def getCiphertextPair(cc):
    c = cc[:]
    cs = [getCiphertext(ct) for ct in c]
    return cs


def getBinaryPairs(lnc, cnc):
    ln = lnc[:]
    cn = cnc[:]
    p = [applyPerm(encode(l), ip, 64) for l in ln]
    cs = getCiphertextPair(cn)
    return [p, cs]


def getBinaryForm(plainc, cipherc):
    plain = plainc[:]
    cipher = cipherc[:]
    p = applyPerm(encode(plain), ip, 64)
    c = getCiphertext(cipher)
    return [p, c]


def main():
    p = generatePair(['ffffffff', 'ghihkftughghijkl'])
    print(p)
    ps = [encode(pt) for pt in p]
    print(ps[0])
    print(ps[1])

    cn = ['pghmimpgknfpngtf', 'tltnhlnjgonfktnr']
    cs = getCiphertextPair(cn)
    # print(cs[0])
    # print(cs[1])

    # print(p)
    # print(c)


if __name__ == '__main__':
    main()
