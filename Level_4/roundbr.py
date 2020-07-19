from test import getSBoxInverse
from constants import sBoxes
from des import expandBlock
from cio import encode
from utils import xor, applyPerm, toNumber, toBinary
from third import INV_PERM, PAIRS, extractCommon

# sBoxInv = getSBoxInverse(sBoxes[4])


def getKeyPossesForBlock(L0, R0, L1, R1, sBoxId):
    sBoxInv = getSBoxInverse(sBoxes[sBoxId])
    afP = xor(R1, L0)
    befPFull = applyPerm(afP, INV_PERM, 32)
    befP = befPFull[sBoxId*4:sBoxId*4+4]
    print("==")
    print(befP)
    # print("~~")
    # print(befP)
    sbOnum = toNumber(list(reversed(befP)))
    afKey = [list(reversed(toBinary(k, 6))) for k in sBoxInv[sbOnum]]
    print(afKey)
    print("==")
    befKey = expandBlock(R0)[sBoxId*6:sBoxId*6+6]
    keyPosses = [xor(befKey, k) for k in afKey]
    return keyPosses


def getRoundKeyBlock(pairs, sBoxId):
    keyPosses = []
    # print(len(pairs))
    # print(pairs[0][1])
    # print(pairs[1][1])
    for pair in pairs:
        L0, R0 = pair[0][:32], pair[0][32:]
        L1, R1 = pair[1][:32], pair[1][32:]
        print(L1, R1)
        posses = getKeyPossesForBlock(L0, R0, L1, R1, sBoxId)
        keyPosses.append(posses)
    keyBlock = extractCommon(keyPosses)
    print(keyPosses)
    print(keyBlock)
    return keyBlock


def getRoundKey(pairs):
    key = []
    for sBoxId in range(8):
        keyBlock = getRoundKeyBlock(pairs, sBoxId)
        if len(keyBlock) > 1:
            raise ValueError("More pairs needed to break round")
        else:
            print(keyBlock)
            key += keyBlock[0]
    return key


# p1 = [i % 2 for i in range(64)]
# c1 = [(1-i % 2) for i in range(64)]
# pairs = [[p1, c1] for i in range(4)]

# L0 = p1[:32]
# L1 = c1[:32]
# R0 = p1[32:]
# R1 = c1[32:]

# print(getKeyPossesForBlock(L0, R0, L1, R1, 4))
# print(getRoundKeyBlock(pairs, 4))
# print(getRoundKey(pairs))
