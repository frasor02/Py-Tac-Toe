import socket
from _thread import *
import pickle
import traceback
import os
from tic_tac_toe import TicTacToe_Server

BUFSIZE = 2048
INF = float('inf')
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)



class Server:
    def __init__(self):
        self.server = ''
        self.port = 10000 or os.environ['PORT']
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.bind((self.server, self.port))
        except:
            print("Bind failed")

        self.server_socket.listen()
        print("Waiting for a connection, server started...")

        self.connected = set()
        self.games = {}
        self.id_count = 0


    def threaded_client(self, connection, player , game_id):
        connection.send(str.encode(str(player)))
        reply = ""

        while True:
            try:
                data = connection.recv(BUFSIZE * 2).decode()
                if game_id in self.games.keys(): # Check if games still exists
                    game = self.games[game_id]
                    if not data:
                        print("Data inconsistent")
                        break
                    else:
                        if data == "reset":
                            self.games[game_id] = TicTacToe_Server(game_id) # Reset current match
                        elif data != "get": # If a move is received
                            data = tuple(map(int, data[1:4].split(',')))
                            game.play(player, data)
                        reply = game
                        connection.sendall(pickle.dumps(reply))
                else:
                    print("Game does not exist")
                    break
            except:
                traceback.print_exc()
                break
        
        print("Lost connection")
        try:
            del self.games[game_id]
            print("Closing game", game_id)
        except:
            self.id_count -= 1
            connection.close()
            return
        self.id_count -= 1
        connection.close()
    
    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            print("Connected to:", addr)

            self.id_count += 1 # Add one to number of clients connected
            player = 0
            game_id = (self.id_count - 1) // 2 # Every two people connected gameId goes up by one
            print(game_id, self.id_count)
            if self.id_count % 2 == 1: # If we need to create a new game
                self.games[game_id] = TicTacToe_Server(game_id) # Create a new Tic Tac Toe Multiplayer
                print("Creating a new game...")
            else:
                self.games[game_id].ready = True
                player = 1

            start_new_thread(self.threaded_client, ((conn, player, game_id)))


if __name__ == '__main__':
    server = Server()
    server.run()
