import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

class Text:
    def __init__(self, screen, text, font, fontsize,color, x_pos, y_pos):
        self.screen = screen
        self.text = pg.font.SysFont(font, fontsize).render(text, True, color)
        self.rect = self.text.get_rect(center=(x_pos, y_pos))

    def draw(self):
        self.screen.blit(self.text, self.rect)