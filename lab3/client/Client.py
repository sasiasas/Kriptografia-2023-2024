import collections
import socket
import datetime
import threading
import random

from merklehellman.MerkleHellman import MerkleHellman
from solitaire.Solitaire import Solitaire

Peer = collections.namedtuple('Peer', 'port public_key')

"""
Class used to represent the Client.
"""


class Client(threading.Thread):
    def __init__(self, client_name=None):
        threading.Thread.__init__(self)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_port = None

        self.peer_socket = None
        self.threads = []

        self.peers = dict()
        self.name = client_name
        self.private_key = None
        self.public_key = None

        self.stop = False

        self.initial_deck = list(range(1, 55))
        self.solitaire = None

    def log(self, msg):
        print('{} [CLIENT {}]: {}'.format(datetime.datetime.now(), self.name, msg))

    def generate_key_pair(self):
        """
        Generate private and public keys and store them.
        """
        keys = MerkleHellman.generate_keys(8)
        self.private_key = keys.private_key
        self.public_key = keys.public_key

    def register_public_key(self):
        """
        Register the public key(save it on the KeyServer side).
        :return: True if the registration was successful, otherwise False.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8029))
        sock.send('SUBSCRIBE {} {}'.format(self.name, ",".join(str(i) for i in self.public_key)).encode())
        res = sock.recv(4096).decode()
        sock.close()
        if 'OK' in res:
            self.listen_port = int(res.split()[1])
            return True
        return False

    def get_client_public_key(self, client_name):
        """

        :param client_name: Get the public key of a client registered on the KeyServer.
        :return: Port and public key of the requested client.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8029))
        sock.send('REQUEST {}'.format(client_name).encode())
        res = sock.recv(4096).decode()
        self.peers[client_name] = Peer(int(res.split()[0]), [int(s) for s in res.split()[1].split(',')])
        sock.close()
        return res

    def connect(self, client_name):
        """
        Connect to another client.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self.peers[client_name].port))
        self.peer_socket = sock

    def send_solitaire_message(self, client_name, msg):
        """
        Send Solitaire encrypted message.
        :param client_name: Name of the other client(peer).
        :param msg: Message string.
        """
        if self.solitaire is None:
            self.solitaire = Solitaire(self.initial_deck)
        msg = self.solitaire.encrypt(msg)
        self.peer_socket.send(('sol#' + str(MerkleHellman.encrypt(msg, self.peers[client_name].public_key))).encode())

    def send_message(self, client_name, msg):
        """
        Send non-encrypted message.
        :param client_name: Name of the other client(peer).
        :param msg: Message string.
        """
        self.peer_socket.send(('plain#' + str(MerkleHellman.encrypt(msg, self.peers[client_name].public_key))).encode())

    def send_init_message(self, client_name, msg):
        """
        Send init(initialize Solitaire deck) message.
        :param client_name: Name of the other client(peer).
        :param msg: Message string.
        """
        self.peer_socket.send(('deck#' + str(MerkleHellman.encrypt(msg, self.peers[client_name].public_key))).encode())

    def generate_initial_deck(self, seed):
        """
        Shuffle the deck based on the random seed.
        :param seed: Random seed.
        """
        random.seed(seed)
        random.shuffle(self.initial_deck)

    def __handle_connection(self, conn, addr):
        while not self.stop:
            data = self.peer_socket.recv(4096)
            msg = data.decode()
            if msg == '':
                continue
            try:
                if msg.split('#')[0] == 'deck':
                    msg = msg.split('#')[1]
                    seed = int(MerkleHellman.decrypt([int(s) for s in msg[1:-1].split(',')], self.private_key))
                    self.log("Initial deck seed received: " + str(seed))
                    self.generate_initial_deck(seed)
                if msg.split('#')[0] == 'plain':
                    msg = msg.split('#')[1]
                    self.log("Message received: " + MerkleHellman.decrypt([int(s) for s in msg[1:-1].split(',')],
                                                                          self.private_key))
                if msg.split('#')[0] == 'sol':
                    if self.solitaire is None:
                        self.solitaire = Solitaire(self.initial_deck)
                    msg = msg.split('#')[1]
                    dec_merkle = MerkleHellman.decrypt([int(s) for s in msg[1:-1].split(',')], self.private_key)
                    self.log("Message received: " + self.solitaire.decrypt(dec_merkle))
            except Exception as e:
                self.log("Message received.ERROR: Decoding error. " + e)
                continue

    def run(self):
        self.listen_socket.bind(('localhost', self.listen_port))
        self.listen_socket.listen(5)
        while not self.stop:
            try:
                conn, addr = self.listen_socket.accept()
            except:
                continue
            self.peer_socket = conn
            client_thread = threading.Thread(target=self.__handle_connection, args=(conn, addr,))
            self.threads.append(client_thread)
            client_thread.start()

    def close(self):
        """
        Close the client.
        """
        self.stop = True
        for t in self.threads:
            t.join()
        self.listen_socket.close()
        self.peer_socket.close()
