from api import getCipher
from bruteforce import decrypt
from cio import finalDecode


def main():
    encrPassword = getCipher('password')
    block1 = encrPassword[:16]
    block2 = encrPassword[16:]
    p1 = decrypt(block1)
    p2 = decrypt(block2)
    ans = finalDecode(p1+p2)
    print(ans)


if __name__ == '__main__':
    main()
