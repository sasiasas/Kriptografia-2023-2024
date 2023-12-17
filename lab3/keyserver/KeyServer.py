import collections
import socket
import threading
import datetime

Client = collections.namedtuple('Client', 'port public_key')

"""
Class used to represent the KeyServer.
"""


class KeyServer(threading.Thread):
    def __init__(self, address, port):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.users = dict()
        self.stop = False
        self.current_port = self.port + 60

    def log(self, msg):
        print('{} [KEY SERVER]: {}'.format(datetime.datetime.now(), msg))

    def __handle_client(self, conn, addr):
        self.log('Handling client:' + str(addr))

        while True:
            data = conn.recv(4096)
            msg = data.decode()
            if "SUBSCRIBE" in msg:
                public_key = msg.split()[2].split(',')
                self.users[msg.split()[1]] = Client(self.current_port, public_key)
                self.log('User ' + msg.split()[1] + ' subscribed.')
                conn.send(('OK ' + str(self.current_port)).encode())
                self.current_port += 1
            if "REQUEST" in msg:
                self.log('User requested: ' + msg.split()[1])
                if msg.split()[1] in self.users.keys():
                    public_key = ",".join(self.users[msg.split()[1]].public_key)
                    conn.send((str(self.users[msg.split()[1]].port) + ' ' + public_key).encode())

    def run(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen(5)
        while not self.stop:
            conn, addr = self.socket.accept()
            client_thread = threading.Thread(target=self.__handle_client, args=(conn, addr,))
            client_thread.start()
        self.socket.close()

    def close(self):
        self.stop = True
