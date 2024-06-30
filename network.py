# Module that handles connection from client to server providing useful functions

import socket
import pickle


BUFSIZE = 2048

class Network:
    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(BUFSIZE).decode()
        except:
            print("recv failed in connect function")
            return

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(BUFSIZE))
        except:
            print("send failed")
            pass
    