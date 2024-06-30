# Module that handles the game logic

# Importing modules
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from random import randint
from button import Button
from minimax import Minimax


# Constants
WIN_SIZE = 600
CELL_SIZE = WIN_SIZE / 3
CELL_CENTER = pg.math.Vector2(CELL_SIZE / 2)
INF = float('inf')
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class TicTacToe:
    def __init__(self, screen):
        self.screen = screen
        self.game_array = []
        for x in range(3):
            row = [INF] * 3
            self.game_array.append(row)
        self.player = randint(0, 1) # Variable that keeps track of whose turn is this

        # All possible winning lines in game array
        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)], 
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1,1), (2, 0)]]
        self.winner = None
        self.game_steps = 0

        self.buttons = []
        self.buttons.append(Button(self.screen, BLACK, WIN_SIZE + 300, CELL_SIZE + 50, "Restart", "white"))
        self.buttons.append(Button(self.screen, BLACK, WIN_SIZE + 300, CELL_SIZE + 200, "Main menu", "white"))

    
    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum(self.game_array[i][j] for i, j in line_indices)
            if sum_line in {0, 3}:
                self.winner = "XO"[sum_line == 0]
                self.winner_line = [pg.math.Vector2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    pg.math.Vector2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER,]


    def run_game_events(self, event):
        current_cell = pg.math.Vector2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)

        # Check if index is out of range
        if col not in range(0, len(self.game_array)):
            return
        if row not in range(0, len(self.game_array)):
            return

        if self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    if obj:
                        pg.draw.line(self.screen, GREEN, (x * CELL_SIZE + (0.15 * CELL_SIZE), y * CELL_SIZE + (0.15 * CELL_SIZE)), (x * CELL_SIZE + (0.85 * CELL_SIZE), y * CELL_SIZE + (0.85 * CELL_SIZE)), int(CELL_SIZE // 8))
                        pg.draw.line(self.screen, GREEN, (x * CELL_SIZE + (0.15 * CELL_SIZE), y * CELL_SIZE + (0.85 * CELL_SIZE)), (x * CELL_SIZE + (0.85 * CELL_SIZE), y * CELL_SIZE + (0.15 * CELL_SIZE)), int(CELL_SIZE // 8))
                    else:
                        pg.draw.circle(self.screen, YELLOW, (x * CELL_SIZE + CELL_SIZE/2, y * CELL_SIZE + CELL_SIZE/2), int(CELL_SIZE // 3))
                        pg.draw.circle(self.screen, WHITE, (x * CELL_SIZE + CELL_SIZE/2, y * CELL_SIZE + CELL_SIZE/2), int(CELL_SIZE // 4))
    
    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.screen, RED, *self.winner_line, 6)

    def print_text(self):
        menu_text = pg.font.SysFont("calibri", 50).render("Tic Tac Toe", True, "black")
        menu_rect = menu_text.get_rect(center=(WIN_SIZE + 300, 50))
        if self.winner:
            info_text = pg.font.SysFont("calibri", 30).render(f'Player "{self.winner}" won!', True, "green")
        elif self.game_steps == 9:
            info_text = pg.font.SysFont("calibri", 30).render(f'Tie!', True, "red")
        else:
            info_text = pg.font.SysFont("calibri", 30).render(f'Player "{"OX"[self.player]}" turn!', True, "black")
        info_rect = info_text.get_rect(center=(WIN_SIZE + 300, CELL_SIZE - 50))
        for text, rect in [(menu_text, menu_rect), (info_text, info_rect)]:
            self.screen.blit(text, rect)
        
        

    def draw(self):
        self.screen.fill(WHITE)
        for x in range(1,3):
            pg.draw.line(self.screen, BLACK, (0, x * CELL_SIZE), (WIN_SIZE, x * CELL_SIZE), 6)
            pg.draw.line(self.screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, WIN_SIZE), 6)
        self.draw_objects()
        self.draw_winner()
        self.print_text()
        for button in self.buttons:
            button.update()
            button.changeColor(pg.mouse.get_pos())
        
    

    def run(self):
        self.draw()



class TicTacToe_Singleplayer(TicTacToe):
    def __init__(self, screen):
        super().__init__(screen)
        self.ai = randint(0, 1)
        self.human = not self.ai
        self.minimax = Minimax(self.ai)
    
    def run_game_events(self, event):
        if self.player == self.human:    
            current_cell = pg.math.Vector2(pg.mouse.get_pos()) // CELL_SIZE
            col, row = map(int, current_cell)

            # Check if index is out of range
            if col not in range(0, len(self.game_array)):
                return
            if row not in range(0, len(self.game_array)):
                return

            if self.game_array[row][col] == INF and not self.winner:
                self.game_array[row][col] = self.player
                self.player = not self.player
                self.game_steps += 1
                self.check_winner()
    
    def print_text(self):
        menu_text = pg.font.SysFont("calibri", 50).render("Tic Tac Toe", True, "black")
        menu_rect = menu_text.get_rect(center=(WIN_SIZE + 300, 50))
        if self.winner:
            info_text = pg.font.SysFont("calibri", 30).render(f'Player "{self.winner}" won!', True, "green")
        elif self.game_steps == 9:
            info_text = pg.font.SysFont("calibri", 30).render(f'Tie!', True, "red")
        else:
            info_text = pg.font.SysFont("calibri", 30).render(f'You are "{"OX"[self.human]}" and "{"OX"[self.ai]}" is AI!', True, "black")
        info_rect = info_text.get_rect(center=(WIN_SIZE + 300, CELL_SIZE - 50))
        for text, rect in [(menu_text, menu_rect), (info_text, info_rect)]:
            self.screen.blit(text, rect)

    def run(self):
        super().run()
        if self.player == self.ai:
            move = self.minimax.best_move(self.game_array)
            if self.game_array[move[0]][move[1]] == INF and not self.winner:
                self.game_array[move[0]][move[1]] = self.player
                self.player = not self.player
                self.game_steps += 1
                self.check_winner()





# Class that handles client connection to server
class TicTacToe_Multiplayer(TicTacToe):
    def __init__(self, screen, game_id):
        super().__init__(screen)
        self.ready = False
        self.game_id = game_id
        self.player_id = float('inf')
    
    def set_player_id(self, player_id):
        self.player_id = player_id
    
    def update_from_server(self, data): # Transfer information from server object to client object
        self.game_array = data.game_array
        self.player = data.player
        self.ready = data.ready
        self.game_id = data.game_id
        self.winner = data.winner
        self.winner_line = data.winner_line
        self.game_steps = data.game_steps

    def run_game_events(self, event, network):
        if self.player == self.player_id: # If it's my turn
            # communicate move to server
            current_cell = pg.math.Vector2(pg.mouse.get_pos()) // CELL_SIZE
            col, row = map(int, current_cell)

            # Check if index is out of range
            if col not in range(0, len(self.game_array)):
                return
            if row not in range(0, len(self.game_array)):
                return

            if self.game_array[row][col] == INF and not self.winner:
                network.send("(" + str(row) + "," + str(col) + ")")

    def print_text(self):
        menu_text = pg.font.SysFont("calibri", 50).render("Tic Tac Toe", True, "black")
        menu_rect = menu_text.get_rect(center=(WIN_SIZE + 300, 50))
        turn_text = pg.font.SysFont("calibri", 30).render(f'Player "{"OX"[self.player]}" turn!', True, "black")
        turn_rect = turn_text.get_rect(center=(WIN_SIZE + 300, CELL_SIZE - 100))

        if self.winner:
            info_text = pg.font.SysFont("calibri", 30).render(f'Player "{self.winner}" won!', True, "green")
        elif self.game_steps == 9:
            info_text = pg.font.SysFont("calibri", 30).render(f'Tie!', True, "red")
        else:
            info_text = pg.font.SysFont("calibri", 30).render(f'You are "{"OX"[self.player_id]}" and "{"OX"[not self.player_id]}" is Opponent.', True, "black")
        info_rect = info_text.get_rect(center=(WIN_SIZE + 300, CELL_SIZE - 50))
        for text, rect in [(menu_text, menu_rect), (turn_text, turn_rect), (info_text, info_rect)]:
            self.screen.blit(text, rect)

    def connected(self):
        return self.ready

# Class that contains only bare-bones information about the game logic with no graphical interface
class TicTacToe_Server:
    def __init__(self, game_id):
        self.game_array = []
        for x in range(3):
            row = [INF] * 3
            self.game_array.append(row)
        self.player = randint(0, 1) # Variable that keeps track of whose turn it is
        self.ready = False
        self.game_id = game_id
        self.winner = None
        self.game_steps = 0
        self.winner_line = None
        
    
    def play(self, player, move):
        if not self.winner:
            self.game_array[move[0]][move[1]] = player
            self.player = not self.player
            self.game_steps += 1
            self.check_win()

    def check_win(self):
        # All possible winning lines in game array
        line_indices_array = [[(0, 0), (0, 1), (0, 2)], 
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1,1), (2, 0)]]
        for line_indices in line_indices_array:
            sum_line = sum(self.game_array[i][j] for i, j in line_indices)
            if sum_line in {0, 3}:
                self.winner = "XO"[sum_line == 0]
                self.winner_line = [pg.math.Vector2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    pg.math.Vector2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER,]
