import random
import sympy


def goodPrime(p):
    return p % 4 == 3


def findGoodPrime():
    primeNumber = sympy.randprime(100, 1000)
    while not goodPrime(primeNumber):
        primeNumber = sympy.randprime(100, 1000)
    return primeNumber


def blumBlumShub(length):
    q = findGoodPrime()
    p = findGoodPrime()
    n = q * p
    s = random.randint(1, n - 1)

    x = pow(s, 2, n)
    z = ''
    for i in range(length):
        xi = pow(x, 2, n)
        z += str(xi % 2)
        x = xi

    return z


z = blumBlumShub(32)
print(z)
