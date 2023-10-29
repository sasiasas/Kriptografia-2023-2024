#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Sallai Tamas-Levente
SUNet: stim2178
"""
import math
import random
import utils


# CAESAR CIPHER

def encrypt_caesar(plaintext):
    encryption = ""
    for char in plaintext:
        if char.isalpha():
            shifted_char = chr(((ord(char) - ord('A') + 3) % 26) + ord('A'))
            encryption += shifted_char
        else:
            encryption += char

    return encryption


def decrypt_caesar(ciphertext):
    decryption = ""
    for char in ciphertext:
        if char.isalpha():
            shifted_char = chr(abs((ord(char) - ord('A') - 3) % 26) + ord('A'))
            decryption += shifted_char
        else:
            decryption += char

    return decryption


# VIGENERE CIPHER

def encrypt_vigenere(plaintext, keyword):
    encryption = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            shifted_char = chr(
                ((ord(plaintext[i]) - ord('A') + ord(keyword[i % len(keyword)]) - ord('A')) % 26) + ord('A'))
            encryption += shifted_char
        else:
            encryption += plaintext[i]

    return encryption


def decrypt_vigenere(ciphertext, keyword):
    decryption = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shifted_char = chr(
                ((abs(ord(ciphertext[i]) - ord('A')) - ord(keyword[i % len(keyword)]) - ord('A')) % 26) + ord('A'))
            decryption += shifted_char
        else:
            decryption += ciphertext[i]

    return decryption


# SCYTALE CYPHER #
def encrypt_scytale(plaintext, circumference):
    encryption = ""
    for letter_index in range(circumference):
        encryption += plaintext[letter_index::circumference]
    return encryption


def decrypt_scytale(ciphertext, circumference):
    return encrypt_scytale(ciphertext, int(math.ceil(len(ciphertext) / circumference)))


# RAILFENCE CIPHE
def encrypt_railfence(plaintext, rails):
    encryption = ""

    rows = rails
    cols = len(plaintext)

    zigzag = [[0 for j in range(cols)] for i in range(rows)]

    k = 1
    i = 0
    j = 0
    for letter in plaintext:
        zigzag[i][j] = letter
        i += k  # sor valtas
        j += 1  # oszlop valtas
        if i == rows - 1 or i == 0:  # ha a vegenel vagyunk valamelyik sornak iranyt valtunk
            k *= -1

    # felepitjuk a kodolt szoveget
    for i in range(rows):
        for j in range(cols):
            if zigzag[i][j] != 0:
                encryption += zigzag[i][j]

    return encryption


def decrypt_railfence(ciphertext, rails):
    decryption = ""
    rows = rails
    cols = len(ciphertext)

    zigzag = [[0 for j in range(0, cols)] for i in range(0, rows)]

    # beallitjuk a zigzag matrix-ot
    k = 1
    i = 0
    j = 0
    for _ in ciphertext:
        zigzag[i][j] = -1
        i += k
        j += 1
        if i == rows - 1 or i == 0:
            k *= -1

    # felepitjuk a zigzag pattern-t
    index = 0
    for i in range(rows):
        for j in range(cols):
            if zigzag[i][j] == -1:
                zigzag[i][j] = ciphertext[index]
                index += 1

    k = 1
    i = 0
    j = 0
    # felepitjuk a dekodolt szoveget
    for _ in ciphertext:
        decryption += zigzag[i][j]
        i += k
        j += 1
        if i == rows - 1 or i == 0:
            k *= -1

    return decryption


# Merkle-Hellman Knapsack Cryptosystem
""" 1. Build a superincreasing sequence `w` of length n"""
def build_superincreasing_sequence(n):
    w = []
    base = 1

    for _ in range(n):
        next_element = base + sum(w)
        w.append(next_element)
        base = next_element + 1

    return w


def generate_private_key(n=8):
    w = build_superincreasing_sequence(n)

    """2. Choose some integer `q` greater than the sum of all elements in `w`"""
    sum_w = sum(w)
    min_q = sum_w + 1
    max_q = min_q + 100
    q = random.randint(min_q, max_q)

    """3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)"""
    r = 2
    while not utils.coprime(r, q):
        r += 1

    return w, q, r


def create_public_key(private_key):
    w, q, r = private_key

    """beta = (b_1, b_2, ..., b_n) where b_i = r x w_i mod q"""
    beta = [(r * w_i) % q for w_i in w]
    return tuple(beta)


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here


# Caesar Cipher:
plaintext = "PYTHON3"
encryption = encrypt_caesar(plaintext)
print(encryption)
decryption = decrypt_caesar(encryption)
print(decryption)

# Vigenere Cipher:
plaintext = "ATTACKATDAWN"
key = "LEMON"
encryption = encrypt_vigenere(plaintext, key)
print(encryption)
decryption = decrypt_vigenere(encryption, key)
print(decryption)

print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))
print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))

# Railfence Cipher:
plaintext = "WEAREDISCOVEREDFLEEATONCE"
encryption = encrypt_railfence(plaintext, 3)
print(encryption)
decryption = decrypt_railfence(encryption, 3)
print(decryption)

# private_key = generate_private_key()
# print(create_public_key(private_key))
