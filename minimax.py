# Module that handles the singleplayer AI

from random import randint


class Minimax:
    def __init__(self,player):
        self.player = player # Who is the AI player in the current game
    
    def check_win(self, minimax_board, player):
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
            sum_line = sum(minimax_board[i][j] for i, j in line_indices)
            if (sum_line == 0 and player == 0) or (sum_line == 3 and player == 1):
                return True
    
    def check_tie(self, minimax_board):
        for row in minimax_board:
            for cell in row:
                if cell == float('inf'):
                    return False
        return True
    
    def check_empty(self, minimax_board):
        for row in minimax_board:
            for cell in row:
                if cell != float('inf'):
                    return False
        return True

    def minimax(self, minimax_board, depth, is_maximizing):
        # Base cases
        if self.check_win(minimax_board, self.player):
            return float('inf')
        elif self.check_win(minimax_board, not self.player):
            return float('-inf')
        elif self.check_tie(minimax_board):
            return 0
        
        if is_maximizing:
            best_score = -1000 # Initializing
            for row in range(3):
                for col in range(3):
                    if minimax_board[row][col] == float('inf'): # if cell is available
                        minimax_board[row][col] = self.player
                        score = self.minimax(minimax_board, depth + 1, False)
                        minimax_board[row][col] = float('inf')
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = 1000 # Initializing
            for row in range(3):
                for col in range(3):
                    if minimax_board[row][col] == float('inf'): # if cell is available
                        minimax_board[row][col] = not self.player
                        score = self.minimax(minimax_board, depth + 1, True)
                        minimax_board[row][col] = float('inf')
                        best_score = min(best_score, score)
            return best_score
    
    def best_move(self, minimax_board):
        if self.check_empty(minimax_board):
            return (randint(0,2), randint(0,2))

        # Initializing
        best_score = -1000
        best_move = (-1, -1) # invalid move

        for row in range(3):
            for col in range(3):
                if minimax_board[row][col] == float('inf'): # if cell is available
                    minimax_board[row][col] = self.player
                    score = self.minimax(minimax_board, 0, False)
                    minimax_board[row][col] = float('inf')
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        if best_move != (-1, -1):
            return best_move
        else:
            return (0, 0)
