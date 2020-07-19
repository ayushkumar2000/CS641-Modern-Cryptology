from des import _applyOneSBox
from constants import sBoxes, perm, ip, KEY1, KEY2, KEY3
from utils import toBinary, toNumber, applyPerm
from cio import encode, decode
# from third import INV_PERM

INV_PERM = [9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10,
            1, 8, 14, 25, 3, 4, 29, 11, 19, 32, 12, 22, 7, 5, 27, 15, 21, 21]

IP_INVERSE = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21,
              61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]


def getSBoxInverse(sbox):
    res = [[] for i in range(16)]
    for ip in range(64):
        piece = toBinary(ip, 6)
        piece.reverse()
        op = _applyOneSBox(piece, sbox)
        op.reverse()
        opn = toNumber(op)
        res[opn].append(ip)
    return res


# R = getSBoxInverse(sBoxes[4])
# for i in range(len(R)):
#     print("Output: " + str(i))
#     print(R[i])

# s = 'fffffffg'
# se = encode(s)
# # print(len(se))
# p1 = applyPerm(se, IP_INVERSE, 64)
# # print(decode(p1))
# p2 = applyPerm(p1, ip, 64)
# # print(decode(p2))

for key in [KEY1, KEY2, KEY3]:
    k = ''
    for b in key:
        k += str(b)
    print(k)
