import pygame

class Screen:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def getResCenter(self) -> tuple:
        return self.width // 2, self.height // 2