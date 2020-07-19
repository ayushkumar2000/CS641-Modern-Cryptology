from constants import KEY3, KEY2, KEY1, perm
from cio import decode
from textgen import getBinaryForm, getCiphertext
from utils import applyPerm, xor
from des import expandBlock, applySBoxes
from roundbr import getRoundKey, getRoundKeyBlock

INV_PERM = [9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10,
            1, 8, 14, 25, 3, 4, 29, 11, 19, 32, 12, 22, 7, 5, 27, 15, 21, 21]

IP_INVERSE = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21,
              61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]


PAIRS = [['kkggfkffffggfkff', 'tltnhlnjgonfktnr'],
         ['ffjjgjfgkkggfkff', 'qhutmrfklkutnqko'],
         ['kkkkffffffkkffff', 'qkftgtmpmomjfmof'],
         ['fjkggjkkkjfffkgk', 'ruprmjqqqjlpisiu'],
         ['fffffffffgffffff', 'uknmhlqoinjtnjtg'],
         ['gfjjjgjgkkkfkjjk', 'hfglthokimtqrmpf'],
         ['qplljqjgkkmhktjk', 'jfjotnmjhmhtstgq'],
         ['ghihkftughghijkl', 'ohjutjttkppglrkj']]


def encryptDESRound(key, pln):
    L0, R0 = pln[:32], pln[32:]
    e = expandBlock(R0)
    x = xor(key, e)
    s = applySBoxes(x)
    p = applyPerm(s, perm, 32)
    R1 = xor(p, L0)
    L1 = R0
    return L1 + R1


def decryptDESRound(key, cip):
    L1, R1 = cip[:32], cip[32:]
    R0 = L1[:]
    e = expandBlock(R0)
    k = xor(e, key)
    s = applySBoxes(k)
    p = applyPerm(s, perm, 32)
    L0 = xor(p, R1)
    plaintext = L0 + R0
    return plaintext


def getRoundTwoKey():
    binPairs = [getBinaryForm(p[0], p[1]) for p in PAIRS[:]]
    # print(binPairs[0])
    finPairs = []
    for pair in binPairs:
        c2 = decryptDESRound(KEY3, pair[1])
        L0, R0 = pair[0][32:], c2[:32]
        # L1, R1 = c2[:32], c2[32:]
        pair2 = [L0+R0, c2]
        finPairs.append(pair2)
    key2 = getRoundKey(finPairs)
    # key2 = getRoundKeyBlock(finPairs, 7)
    return key2


def getRoundOneKey():
    binPairs = [getBinaryForm(p[0], p[1]) for p in PAIRS[:]]
    # print(binPairs[0])
    finPairs = []
    for pair in binPairs:
        cf = decryptDESRound(KEY3, pair[1])
        c1 = decryptDESRound(KEY2, cf)
        print(c1)
        L0, R0 = pair[0][:32], pair[0][32:]
        # L1, R1 = c2[:32], c2[32:]
        pair2 = [L0+R0, c1]
        finPairs.append(pair2)
    key2 = getRoundKey(finPairs)
    print(finPairs[0][1][:32])
    print(finPairs[1][1][:32])
    # key2 = getRoundKeyBlock(finPairs, 0)
    return key2


def checkFunction():
    binPair = getBinaryForm(PAIRS[0][0], PAIRS[0][1])
    pl2 = decryptDESRound(KEY3, binPair[1])
    pl1 = decryptDESRound(KEY2, pl2)
    cp1 = encryptDESRound(KEY2, pl1)
    cip = encryptDESRound(KEY3, cp1)
    print(binPair[1])
    print(cip)


def breakod(cipher):
    c3 = getCiphertext(cipher)
    c2 = decryptDESRound(KEY3, c3)
    c1 = decryptDESRound(KEY2, c2)
    plain = decryptDESRound(KEY1, c1)
    ans = applyPerm(plain, IP_INVERSE, 64)
    f = decode(ans)
    print(f)


# print(getRoundTwoKey())
# print(getRoundOneKey())
breakod('jfkifgqoorgrrnqn')
breakod('mssiiqislkftkurl')
