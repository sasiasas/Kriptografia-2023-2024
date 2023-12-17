from merklehellman.MerkleHellman import MerkleHellman


def test_merkle_hellman():
    key_length = 8
    keys = MerkleHellman.generate_keys(key_length)

    original_message = "HELLO"

    encrypted_message = MerkleHellman.encrypt(original_message, keys.public_key)

    decrypted_message = MerkleHellman.decrypt(encrypted_message, keys.private_key)

    print("Original Message:", original_message)
    print("Encrypted Message:", encrypted_message)
    print("Decrypted Message:", decrypted_message)

    print("Well Done!") if original_message == decrypted_message else print("Decryption failed!")


test_merkle_hellman()
