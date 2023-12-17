from keyserver.KeyServer import KeyServer
from client.Client import Client
import random
import time

"""
Initializing clients and the KeyServer
"""
key_server = KeyServer('localhost', 8029)
client_1 = Client("Client1")
client_2 = Client("Client2")

try:
    """
    Start the KeyServer
    """
    key_server.start()

    """
    Generate and register public keys for both clients
    """

    client_1.generate_key_pair()
    client_1.register_public_key()
    client_2.generate_key_pair()
    client_2.register_public_key()

    """
    Clients getting each others public key
    """

    client_1.get_client_public_key("Client2")
    client_2.get_client_public_key("Client1")

    """
    Non encrypted communication
    """
    client_1.start()
    client_2.start()
    time.sleep(0.1)

    client_1.connect('Client2')
    time.sleep(0.1)
    client_1.send_message('Client2', 'hello')
    time.sleep(0.1)
    client_2.connect('Client1')
    time.sleep(0.1)
    client_2.send_message('Client1', 'ack1')
    time.sleep(0.1)
    client_1.send_message('Client2', 'szia')
    time.sleep(0.1)
    client_2.send_message('Client1', 'ack2')

    """
    Encrypted communication
    """
    seed = random.randint(1, 10)
    client_1.generate_initial_deck(seed)
    client_1.send_init_message('Client2', str(seed))
    time.sleep(0.1)

    client_1.send_solitaire_message('Client2', 'solitaire')
    time.sleep(0.1)
    client_2.send_solitaire_message('Client1', 'received')
    time.sleep(1)

finally:
    key_server.close()
    client_1.close()
    client_2.close()

