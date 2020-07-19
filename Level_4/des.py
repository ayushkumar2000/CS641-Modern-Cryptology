from constants import sBoxes, expand, perm
from utils import toNumber, toBinary
from keygen import getRoundKeys


def expandBlock(block):
    arr = [block[i-1] for i in expand]
    return arr


def xorKey(block, key):
    arr = []
    for i in range(48):
        arr.append(block[i] ^ key[i])
    return arr


def _applyOneSBox(piece, sbox):
    if len(piece) != 6:
        raise ValueError('Piece must have 6 elements')
    outer = [piece[0], piece[5]]
    outer.reverse()
    inner = piece[1:5]
    inner.reverse()
    number = sbox[toNumber(outer)][toNumber(inner)]
    output = toBinary(number, 4)
    output.reverse()
    return output


def applySBoxes(block):
    pieces = [block[i:i+6] for i in range(0, 48, 6)]
    reducedPieces = [_applyOneSBox(pieces[i], sBoxes[i]) for i in range(8)]
    result = []
    for piece in reducedPieces:
        result += piece
    return result


def permute(block):
    result = [block[perm[i] - 1] for i in range(32)]
    return result


def applyDESFunc(block, key):
    if len(block) != 32:
        raise ValueError('Half-block must be exactly 32 bits long.')
    block = expandBlock(block)
    block = xorKey(block, key)
    block = applySBoxes(block)
    block = permute(block)
    return block


def xorHalves(left, right):
    result = [left[i] ^ right[i] for i in range(32)]
    return result


def encryptOneRound(text, roundKey):
    if len(text) != 64:
        raise ValueError('Round plaintext must be exactly 64 bits long.')
    left = text[:32]
    right = text[32:]
    processedRight = applyDESFunc(right, roundKey)
    finalRight = xorHalves(left, processedRight)
    result = right + finalRight
    return result


def encryptBlock(plaintext, numOfRounds, fullKey):
    # Add input and output permutation steps
    if len(plaintext) != 64:
        raise ValueError('Plaintext must be exactly 64 bits long.')
    roundKeys = getRoundKeys(fullKey)
    currText = plaintext
    for round in range(numOfRounds):
        currText = encryptOneRound(currText, roundKeys[round])
    return currText


def main():
    plaintext = [0 for i in range(32)] + [1 for i in range(32)]
    key = [0 for i in range(64)]
    ciphertext = encryptBlock(plaintext, 1, key)
    print(ciphertext)
