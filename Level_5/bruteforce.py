from api import getCipher
from cio import encode, decode, _toChars
from arithmetic import add, mul, exp


def _genBlockGroup(idx, tillNow):
    res = []
    blocks = [0 for i in range(8)]
    for i in range(len(tillNow)):
        blocks[i] = tillNow[i]
    for i in range(128):
        blocks[idx] = i
        res.append(blocks[:])
    return res


def getIthBlock(i, cipher, tillNow):
    blocks = _genBlockGroup(i, tillNow)
    for block in blocks:
        alpText = encode(block)
        cip = getCipher(alpText)
        if cip[2*i:2*i+2] == cipher[2*i:2*i+2]:
            return block[i]
    raise ValueError("No such block found.")


def decrypt(cipher):
    answer = []
    for i in range(8):
        block = getIthBlock(i, cipher, answer)
        print(f"#{i}: {block}")
        answer.append(block)
    finalAns = encode(answer)
    return finalAns


def main():
    ans = decrypt('lrihgniummflhkio')
    print(ans)


if __name__ == '__main__':
    main()
