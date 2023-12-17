import unittest
import random
from solitaire.Solitaire import Solitaire

class TestSolitaireCommunication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setting up two instances of Solitaire with separate decks
        deck_a = list(range(1, 55))
        random.shuffle(deck_a)
        deck_b = deck_a[:]
        cls.solitaire_a = Solitaire(deck_a)
        cls.solitaire_b = Solitaire(deck_b)

    """
    Stimulus: Encrypt a string and decrypt the encrypted text.
    Reaction: The result should be the same as the initial unencrypted string.
    """
    def test_encrypt_decrypt(self):
        enc = self.solitaire_a.encrypt("test")
        dec = self.solitaire_b.decrypt(enc)
        self.assertEqual(dec, "test")
