import random


def keyGenerator():
    return random.randint(0, 255)


def folyamatTitkosito(byteArray, keyGenerator, seed):
    random.seed(seed)

    newByteArray = []
    for i in byteArray:
        key = keyGenerator()
        newByteArray.append(i ^ key)
    return newByteArray


def main():
    byteArray = b'sziamiau'
    key = 65
    encodedByteArray = folyamatTitkosito(byteArray, keyGenerator, key)

    result = ''
    for i in encodedByteArray:
        result += chr(i)
    print(result)

    decodedByteArray = folyamatTitkosito(encodedByteArray, keyGenerator, key)

    result = ''
    for i in decodedByteArray:
        result += chr(i)
    print(result)


if __name__ == '__main__':
    main()
