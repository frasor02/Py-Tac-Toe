# Module that handles the game application

# Import modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import sys
from tic_tac_toe import *
from button import Button
from network import Network
from text import Text



# Constants
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE, WIN_SIZE])
        pg.display.set_caption("Tic Tac Toe")
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self.screen)
        self.tic_tac_toe_singleplayer = TicTacToe_Singleplayer(self.screen)
        self.tic_tac_toe_multiplayer = TicTacToe_Multiplayer(self.screen, 0)


    def new_game(self):
        self.tic_tac_toe = TicTacToe(self.screen)
        self.tic_tac_toe_singleplayer = TicTacToe_Singleplayer(self.screen)
        self.tic_tac_toe_multiplayer = TicTacToe_Multiplayer(self.screen, 0)


        


    def singleplayer(self):
        self.screen = pg.display.set_mode([WIN_SIZE + 500, WIN_SIZE])
        while True:
            self.tic_tac_toe_singleplayer.run()
            for event in pg.event.get():
                if event.type == pg.QUIT: # Check if window is closed
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.tic_tac_toe_singleplayer.buttons[0].checkInput(pg.mouse.get_pos()):
                        self.new_game()
                    if self.tic_tac_toe_singleplayer.buttons[1].checkInput(pg.mouse.get_pos()):
                        self.new_game()
                        self.run()
                    self.tic_tac_toe_singleplayer.run_game_events(event)
            pg.display.update()
            self.clock.tick(60)
    
    def localplay(self):
        self.screen = pg.display.set_mode([WIN_SIZE + 500, WIN_SIZE])
        while True:
            self.tic_tac_toe.run()
            for event in pg.event.get():
                if event.type == pg.QUIT: # Check if window is closed
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.tic_tac_toe.buttons[0].checkInput(pg.mouse.get_pos()):
                        self.new_game()
                    if self.tic_tac_toe.buttons[1].checkInput(pg.mouse.get_pos()):
                        self.new_game() # Reset current match before going to main menu
                        self.run()
                    self.tic_tac_toe.run_game_events(event)
            pg.display.update()
            self.clock.tick(60)


    def waiting_players(self, network): # Screen that is seen when waiting other players
        waiting = True
        self.screen.fill(WHITE)
        text = Text(self.screen, "Waiting for another player...", "calibri", 50, "black", CELL_SIZE + 400, CELL_SIZE)

        while waiting:
            text.draw()
            try:
                game = network.send("get")
            except:
                print("Couldn't get game")
                return
            self.tic_tac_toe_multiplayer.update_from_server(game)
            if self.tic_tac_toe_multiplayer.ready == True:
                waiting = False

            for event in pg.event.get():
                if event.type == pg.QUIT: # Check if window is closed
                    pg.quit()
                    sys.exit()
            pg.display.update()
            self.clock.tick(60)

        

    def multiplayer(self):
        self.screen = pg.display.set_mode([WIN_SIZE + 500, WIN_SIZE])        
        network = Network('', 5050) # Connection to server
        if network.get_player() == None: # If connection to server fails (i.e. server offline) remain in main menu
            self.run()
            print("no player")

        self.waiting_players(network) # # Waiting for other player if current game is empty

        player = int(network.get_player())
        self.tic_tac_toe_multiplayer.set_player_id(player)
        print("You are player ", player)
        while True:
            try:
                game = network.send("get")
            except:
                print("Couldn't get game")
                self.run()
            if game == None: # If other player disconnects return to main menu
                self.run()
            self.tic_tac_toe_multiplayer.update_from_server(game) # Update with server information
            self.tic_tac_toe_multiplayer.run()
            self.tic_tac_toe_multiplayer.check_winner()

            for event in pg.event.get():
                if event.type == pg.QUIT: # Check if window is closed
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.tic_tac_toe_multiplayer.buttons[0].checkInput(pg.mouse.get_pos()) and (self.tic_tac_toe_multiplayer.winner or self.tic_tac_toe_multiplayer.game_steps == 9):
                        network.send("reset")
                    if self.tic_tac_toe_multiplayer.buttons[1].checkInput(pg.mouse.get_pos()):
                        network.client.close()
                        self.run()
                        print("error desynch")
                    self.tic_tac_toe_multiplayer.run_game_events(event, network)
            pg.display.update()
            self.clock.tick(60)


    def run(self):
        self.screen = pg.display.set_mode([WIN_SIZE, WIN_SIZE])
        self.screen.fill(WHITE)
        text = Text(self.screen, "Tic Tac Toe", "calibri", 50, "black", 300, 100)
        singleplayer_button = Button(self.screen, BLACK, WIN_SIZE/2, WIN_SIZE/2 - 50, "Singleplayer", "white")
        localplay_button = Button(self.screen, BLACK, WIN_SIZE/2, WIN_SIZE/2 + 30, "Local Play", "white")
        multiplayer_button = Button(self.screen, BLACK, WIN_SIZE/2, WIN_SIZE/2 + 120, "Multiplayer", "white")
        quit_button = Button(self.screen, BLACK,  WIN_SIZE/2, WIN_SIZE/2 + 200, "Quit", "white")

        while True:
            text.draw()
            
            for button in [singleplayer_button, localplay_button,multiplayer_button, quit_button]:
                button.changeColor(pg.mouse.get_pos())
                button.update()

            for event in pg.event.get():
                if event.type == pg.QUIT: # Check if window is closed
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if singleplayer_button.checkInput(pg.mouse.get_pos()):
                        self.singleplayer()
                    if localplay_button.checkInput(pg.mouse.get_pos()):
                        self.localplay()
                    if multiplayer_button.checkInput(pg.mouse.get_pos()):
                        self.multiplayer()
                    if quit_button.checkInput(pg.mouse.get_pos()):
                        pg.quit()
                        sys.exit()
            pg.display.update()
            self.clock.tick(60)

