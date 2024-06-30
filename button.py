# Module to create a button with different properties
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg



class Button():
    def __init__(self, screen, color, x_pos, y_pos, text_input, text_color):
        pg.font.init()
        self.screen = screen
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.text = pg.font.SysFont("calibri", 50).render(self.text_input, True, text_color)
        self.rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self):
        pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, self.rect)

    def checkInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = pg.font.SysFont("calibri", 50).render(self.text_input, True, "green")
        else:
            self.text = pg.font.SysFont("calibri", 50).render(self.text_input, True, "white")