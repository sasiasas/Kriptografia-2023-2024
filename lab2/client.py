import socket
import json
import solitaire


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    pakli = list(range(1, 55))

    try:
        while True:
            message = input("Enter your message: ")

            # Encrypt the message and send it
            encrypted_message = solitaire.folyamat_titkosito(message.encode('utf-8'), solitaire.solitaire_key_generator,
                                                             pakli.copy())
            client_socket.sendall(bytes(encrypted_message))

            # Receive the encrypted response
            encoded_data = client_socket.recv(1024)
            if not encoded_data:
                break
            print(f"Received message(encrypted): {encoded_data}")

            # Decrypt the received data
            decrypted_data = solitaire.folyamat_titkosito(encoded_data, solitaire.solitaire_key_generator, pakli.copy())
            decoded_message = ''.join(chr(i) for i in decrypted_data)
            print(f"Received response(decrypted): {decoded_message}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


if __name__ == "__main__":
    start_client()
