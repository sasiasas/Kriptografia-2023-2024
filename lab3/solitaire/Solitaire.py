JOKER_A = 53
JOKER_B = 54


class Solitaire:
    def __init__(self, initial_state):
        assert (isinstance(initial_state, list) and len(initial_state) == 54)
        self.deck = initial_state

    def __find_and_move_joker_a(self):
        pos = self.deck.index(JOKER_A)
        if pos == len(self.deck) - 1:
            self.deck.pop(pos)
            self.deck.insert(1, JOKER_A)
        else:
            self.deck[pos], self.deck[pos + 1] = self.deck[pos + 1], self.deck[pos]

    def __find_and_move_joker_b(self):
        pos = self.deck.index(JOKER_B)
        if pos == len(self.deck) - 1:
            self.deck.pop(pos)
            self.deck.insert(2, JOKER_B)
        else:
            if pos == len(self.deck) - 2:
                self.deck.pop(pos)
                self.deck.insert(1, JOKER_B)
            else:
                self.deck[pos], self.deck[pos + 2] = self.deck[pos + 2], self.deck[pos]

    def __perform_triple_cut(self):
        pos_a = self.deck.index(JOKER_A)
        pos_b = self.deck.index(JOKER_B)
        if pos_a < pos_b:
            self.deck = self.deck[(pos_b + 1):] + self.deck[pos_a:pos_b + 1] + self.deck[0:pos_a]
        else:
            self.deck = self.deck[(pos_a + 1):] + self.deck[pos_b:pos_a + 1] + self.deck[0:pos_b]

    def __perform_count_cut(self):
        return self.deck[self.deck[0] - 1]

    def __get_key_stream_element(self):
        res = JOKER_A
        while (res == JOKER_A) or (res == JOKER_B):
            self.__find_and_move_joker_a()
            self.__find_and_move_joker_b()
            self.__perform_triple_cut()
            res = self.__perform_count_cut()
        return res

    def encrypt(self, msg):
        enc = ''
        for char in msg:
            key_stream_value = self.__get_key_stream_element()
            enc += chr(96 + ((ord(char) - 96) + key_stream_value) % 26)
        return enc

    def decrypt(self, msg):
        dec = ''
        for char in msg:
            key_stream_value = self.__get_key_stream_element()
            value = (ord(char) - 96) - key_stream_value
            while value <= 0:
                value += 26
            dec += chr(96 + value)
        return dec




