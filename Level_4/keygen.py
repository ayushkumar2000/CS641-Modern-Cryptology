from constants import pc1, pc2, shifts
from utils import rotateHalves


def applyPC1(key):
    if len(key) != 64:
        raise ValueError('Key must have exactly 64 elements (bits)')
    result = [key[pc1[i] - 1] for i in range(56)]
    return result


def applyPC2(key):
    if len(key) != 56:
        raise ValueError('Key must have exactly 56 elements (bits)')
    result = [key[pc2[i] - 1] for i in range(48)]
    return result


def getRoundKeys(fullKey):
    keys = []
    # key_PC1 = applyPC1(fullKey)
    key_PC1 = fullKey
    currKey = key_PC1
    for i in range(16):
        rotated = rotateHalves(currKey, shifts[i])
        newKey = applyPC2(rotated)
        keys.append(newKey)
        currKey = rotated
    return keys
