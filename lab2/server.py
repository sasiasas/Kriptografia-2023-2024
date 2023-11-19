import socket
import json
import solitaire


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Server is listening for incoming connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        pakli = list(range(1, 55))

        try:
            while True:
                encoded_data = client_socket.recv(1024)

                if not encoded_data:
                    break

                print(f"Received message(encrypted): {encoded_data}")

                decrypted_data = solitaire.folyamat_titkosito(encoded_data, solitaire.solitaire_key_generator,
                                                              pakli.copy())
                decoded_message = ''.join(chr(i) for i in decrypted_data)
                print(f"Received response(decrypted): {decoded_message}")

                message = input("Enter your response: ")

                # Encrypt the message and send it
                encrypted_message = solitaire.folyamat_titkosito(message.encode('utf-8'),
                                                                 solitaire.solitaire_key_generator, pakli.copy())
                client_socket.sendall(bytes(encrypted_message))

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()
            print("Connection closed.")


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config


if __name__ == "__main__":
    start_server()
