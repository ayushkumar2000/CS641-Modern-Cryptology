def toBinary(n, padTo):
    arr = []
    while n != 0:
        arr.append(n % 2)
        n //= 2
    while len(arr) < padTo:
        arr.append(0)
    return arr


def toNumber(bits):
    if len(bits) == 0:
        return 0
    else:
        n = 0
        i = 0
        for bit in bits:
            n += bit*(2**i)
            i += 1
        return n


def equals(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True


def rotateLeft(arr, offset):
    result = arr[offset:] + arr[:offset]
    return result


def rotateHalves(arr, offset):
    length = len(arr)//2
    result = rotateLeft(arr[:length], offset) + \
        rotateLeft(arr[length:], offset)
    return result


def xor(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError("Length of the lists must be same")
    res = [arr1[i] ^ arr2[i] for i in range(len(arr1))]
    return res


def applyPerm(arr, perm, n):
    res = [arr[perm[i]-1] for i in range(n)]
    return res
