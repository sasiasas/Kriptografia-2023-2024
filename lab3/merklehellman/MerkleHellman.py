import random
import collections
from math import gcd

Keys = collections.namedtuple('Keys', 'public_key private_key')
PrivateKey = collections.namedtuple('PrivateKey', 'w q r')


class MerkleHellman:
    @staticmethod
    def __build_super_increasing_sequence(start, n):
        seq = [start]
        total = start

        # Generate n - 1 random elements and add them to the sequence
        for i in range(n - 1):
            element = random.randint(total + 1, total * 2)
            total = total + element
            seq.append(element)
        return seq

    @staticmethod
    def generate_keys(n):

        w = MerkleHellman.__build_super_increasing_sequence(random.randint(1, 2), n)
        w_sum = sum(w)
        q = random.randint(w_sum + 1, w_sum * 2)
        r = random.randint(2, q - 1)

        # Ensure 'r' and 'q' are coprime
        while gcd(r, q) != 1:
            r = random.randint(2, q - 1)

        beta = [r * w_i % q for w_i in w]
        # Return the keys (public and private)
        return Keys(beta, PrivateKey(w, q, r))

    @staticmethod
    def __encrypt_character(char, public_key):
        # Convert the character to a binary representation
        binary_representation = [1 if ord(char) & (1 << (7 - n)) else 0 for n in range(8)]

        # Perform the encryption using the public key
        encrypted_value = sum([binary_bit * public_key_bit for binary_bit, public_key_bit in zip(binary_representation, public_key)])

        # Return the encrypted value
        return encrypted_value

    # (a * x) mod m = 1 -> x is the modular inverse of 'a' modulo 'm'
    @staticmethod
    def __mod_inverse(a, m):
        m0 = m
        y = 0
        x = 1

        if m == 1:
            return 0

        while a > 1:
            q = a // m
            t = m
            m = a % m
            a = t
            t = y
            y = x - q * y
            x = t
        if x < 0:
            x = x + m0

        return x

    @staticmethod
    def __super_increasing_knapsack(target_sum, sequence):
        remaining_sum = target_sum
        solution = []

        # Iterate from right -> left
        for value in reversed(sequence):
            # Include the value if it doesn't exceed the remaining sum
            if value <= remaining_sum:
                solution.append(1)
                remaining_sum -= value
            else:
                solution.append(0)

        # Check if the target sum is reached
        if remaining_sum == 0:
            solution.reverse()  # Reverse the solution list to maintain original order
            return solution  # Return the solution

        return None  # or none if the target sum cannot be reached

    @staticmethod
    def decrypt(enc, private_key):
        # Calculating the modular inverse 's'
        s = MerkleHellman.__mod_inverse(private_key.r, private_key.q)

        # Decrypting the ciphertext 'enc'
        decrypted_values = [(enc_i * s) % private_key.q for enc_i in enc]

        # Converting decrypted values to characters
        decrypted_message = ""
        for decrypted_value in decrypted_values:
            binary_representation = MerkleHellman.__super_increasing_knapsack(decrypted_value, private_key.w)
            integer_value = int("".join(map(str, binary_representation)), 2)
            decrypted_message += chr(integer_value)

        # Return the decrypted message
        return decrypted_message

    @staticmethod
    def encrypt(msg, public_key):
        return [MerkleHellman.__encrypt_character(char, public_key) for char in msg]

