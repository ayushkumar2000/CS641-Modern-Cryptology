from utils import xor, toNumber, toBinary, applyPerm, equals
from des import expandBlock, applySBoxes, _applyOneSBox
from constants import sBoxes
from textgen import getBinaryPairs
from test import getSBoxInverse

INV_PERM = [9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10,
            1, 8, 14, 25, 3, 4, 29, 11, 19, 32, 12, 22, 7, 5, 27, 15, 21, 21]

PAIRS = [[['ffffffffffffffff', 'fgffffffffffffff'],
          ['pghmimpgknfpngtf', 'pjhomlmsksgpnkns']],
         [['ffffffffffffffff', 'fffffffffgffffff'],
          ['pghmimpgknfpngtf', 'uknmhlqoinjtnjtg']],
         [['ffffffffffffffff', 'kkggfkffffggfkff'],
          ['pghmimpgknfpngtf', 'tltnhlnjgonfktnr']],
         [['ffffffffffffffff', 'ffjjgjfgkkggfkff'],
          ['pghmimpgknfpngtf', 'qhutmrfklkutnqko']],
         [['ffffffffffffffff', 'kkkkffffffkkffff'],
          ['pghmimpgknfpngtf', 'qkftgtmpmomjfmof']],
         [['kkkkffffffkkffff', 'fjkggjkkkjfffkgk'],
          ['qkftgtmpmomjfmof', 'ruprmjqqqjlpisiu']],
         [['kkkkffffffkkffff', 'ffjjgjfgkkggfkff'],
          ['qkftgtmpmomjfmof', 'qhutmrfklkutnqko']],
         [['kkkkffffffkkffff', 'kkggfkffffggfkff'],
          ['qkftgtmpmomjfmof', 'tltnhlnjgonfktnr']],
         [['kkkkffffffkkffff', 'fgffffffffffffff'],
          ['qkftgtmpmomjfmof', 'pjhomlmsksgpnkns']],
         [['kkkkffffffkkffff', 'fffffffffgffffff'],
          ['qkftgtmpmomjfmof', 'uknmhlqoinjtnjtg']]
         ]


def getXorInverse(res, numOfBits):
    poss = []
    res.reverse()
    # print(res)
    res = toNumber(res)
    n = 2**numOfBits
    for i in range(n):
        for j in range(n):
            if i ^ j == res:
                ib = toBinary(i, numOfBits)
                jb = toBinary(j, numOfBits)
                ib.reverse()
                jb.reverse()
                poss.append([ib, jb])
    return poss


def getSBoxInputs(sbox, iXor, oXor):
    sboxInv = getSBoxInverse(sbox)
    allPosses = getXorInverse(oXor[:], 4)
    ipPosses = []
    for poss in allPosses:
        alpha, beta = poss
        alpha.reverse()
        beta.reverse()
        gss = sboxInv[toNumber(alpha)]
        dss = sboxInv[toNumber(beta)]
        gammas = [list(reversed(toBinary(g, 6))) for g in gss]
        deltas = [list(reversed(toBinary(d, 6))) for d in dss]
        for g in gammas:
            for d in deltas:
                x = xor(g, d)
                if equals(x, iXor):
                    ipPosses.append([g, d])
    return ipPosses


def filterPoss(posses, opxor, sbox):
    res = []
    for poss in posses:
        ops = [_applyOneSBox(p, sbox) for p in poss]
        gOpxor = xor(ops[0], ops[1])
        matches = True
        for i in range(len(gOpxor)):
            if gOpxor[i] != opxor[i]:
                matches = False
                break
        if matches:
            res.append(poss)
    return res


def getDeltas(pairs):
    '''
    Returns del(L0), del(R2) and del(R3)
    '''
    P1, P2 = pairs[0]
    C1, C2 = pairs[1]
    L01 = P1[:32]
    L02 = P2[:32]
    L31 = C1[:32]
    L32 = C2[:32]
    R31 = C1[32:]
    R32 = C2[32:]
    L0d = xor(L01, L02)
    R2d = xor(L31, L32)
    R3d = xor(R31, R32)
    return L0d, R2d, R3d


def getSBoxIO(deltas):
    '''
    Returns input block and output block of S-Boxes
    '''
    L0d, R2d, R3d = deltas
    permO = xor(R3d, L0d)
    sboxO = applyPerm(permO, INV_PERM, 32)
    sboxI = expandBlock(R2d)
    return sboxI, sboxO


def getAfterKeyPossesForPair(sboxI, sboxO, sBoxId):
    ip = sboxI[sBoxId*6:sBoxId*6 + 6]
    op = sboxO[sBoxId*4:sBoxId*4 + 4]
    posses = getSBoxInputs(sBoxes[sBoxId], ip[:], op[:])
    return posses


def getKeyBlockPoss(afKeyPosses, befKey):
    res = []
    for poss in afKeyPosses:
        alpha = poss[0]
        key1 = xor(alpha, befKey[0])
        res.append(key1)
    return res


def getKeyBlock(sBoxId):
    pairPosses = []
    for pair in PAIRS:
        binaryPairs = getBinaryPairs(pair[0], pair[1])
        L31, L32 = [c[:32] for c in binaryPairs[1]]
        beforeKey = [expandBlock(d) for d in [L31, L32]]
        deltas = getDeltas(binaryPairs)
        sboxI, sboxO = getSBoxIO(deltas)
        allPosses = getAfterKeyPossesForPair(sboxI, sboxO, sBoxId)
        befKey = [k[sBoxId*6:sBoxId*6+6] for k in beforeKey]
        keyPosses = getKeyBlockPoss(allPosses, befKey)
        pairPosses.append(keyPosses)
    res = extractCommon(pairPosses)
    return res


def getKeyThree():
    key3 = []
    for sBoxId in range(8):
        kb = getKeyBlock(sBoxId)[0]
        key3 += kb
    return key3


def extractCommon(lst):
    ls = lst[0]
    res = []
    for l in ls:
        missing = False
        for m in lst:
            if l not in m:
                missing = True
                break
        if not missing:
            res.append(l)
    return res


def main():
    key3 = []
    for sBoxId in range(8):
        kb = getKeyBlock(sBoxId)[0]
        key3 += kb
    print(key3)
    key = ''
    for k in key3:
        key += str(k)
    print("KEY 3: " + key)


if __name__ == '__main__':
    main()
