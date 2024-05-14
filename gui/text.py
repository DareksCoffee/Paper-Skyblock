import pygame

class Text:
    def __init__(self):

        pygame.init()

        self.font_size = 12
        self.text_font = pygame.font.Font(".\\assets\\font\\minecraft_font.ttf", self.font_size)