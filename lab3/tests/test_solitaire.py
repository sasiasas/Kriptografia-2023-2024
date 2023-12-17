from solitaire.Solitaire import Solitaire
import unittest
import random


class TestSolitaire(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initial_deck = list(range(1, 55))
        random.shuffle(initial_deck)
        cls.solitaire = Solitaire(initial_deck)

    """
    Stimulation: Encrypt the lowercase test string using the algorithm.
    Reaction   : Encrypted string contains only English lowercase letters.
    """
    def test_encrypt(self):
        enc = self.solitaire.encrypt('test')
        self.assertEqual(enc.islower(), True)

    """
    Stimulation: Decrypt the lowercase test string using the algorithm.
    Reaction   : Decrypted string contains only English lowercase letters.
    """
    def test_decrypt(self):
        dec = self.solitaire.decrypt('test')
        self.assertEqual(dec.islower(), True)

