def find_joker_index(pakli, joker_value):
    for i in range(len(pakli)):
        if pakli[i] == joker_value:
            return i
    return -1


def move_joker(pakli, joker_value, shift):
    joker_index = find_joker_index(pakli, joker_value)
    if joker_index != -1:
        new_index = (joker_index + shift) % len(pakli)
        pakli[joker_index], pakli[new_index] = pakli[new_index], joker_value


def rearrange_cards(pakli, start, end):
    return pakli[end + 1:] + pakli[start:end + 1] + pakli[:start]


def solitaire(pakli):
    # Move White Joker
    move_joker(pakli, 53, 1)

    # Move Black Joker
    move_joker(pakli, 54, -2 if find_joker_index(pakli, 54) == 52 else -1)

    # Rearrange cards between two Jokers
    elso = find_joker_index(pakli, 53)
    masodik = find_joker_index(pakli, 54)
    pakli = rearrange_cards(pakli, elso, masodik)

    # Move the last card to its appropriate position
    if pakli[-1] not in [53, 54]:
        utolso = pakli[-1]
        pakli = rearrange_cards(pakli, utolso, 53)

    # Find the key card and return it along with the modified pakli
    elso = pakli[0] if pakli[0] != 54 else 53
    kulcs = pakli[elso]
    return kulcs, pakli


def solitaire_key_generator(pakli):
    kulcs1, pakli = solitaire(pakli)
    kulcs2, pakli = solitaire(pakli)
    kulcs = (kulcs1 * kulcs2) % 256
    return kulcs, pakli


def folyamat_titkosito(byteArray, key_generator, pakli):
    new_byte_array = [i ^ key_generator(pakli)[0] for i in byteArray]
    return new_byte_array


def main():
    initial_deck = list(range(1, 55))

    pakli = initial_deck.copy()
    byteArray = b'kutya fule'

    encoded_byte_array = folyamat_titkosito(byteArray, solitaire_key_generator, pakli)

    encoded_message = ''.join(chr(i) for i in encoded_byte_array)
    print(encoded_message)

    pakli = initial_deck.copy()
    decoded_byte_array = folyamat_titkosito(encoded_byte_array, solitaire_key_generator, pakli)

    decoded_message = ''.join(chr(i) for i in decoded_byte_array)
    print(decoded_message)


if __name__ == '__main__':
    main()
