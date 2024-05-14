import pygame
from gui.text import Text

class InputBox:
    def __init__(self, screen):
        self.screen = screen

        self.text = Text()
        self.font = self.text.text_font

        self.text_color = (255, 255, 255)
        self.background_color = (50, 50, 50, 180)

    
    def displayInput(self, input_text: str) -> None:
        input_box_height = 25

        background_surface = pygame.Surface((self.screen.get_width() - 20, input_box_height), pygame.SRCALPHA)
        background_surface.fill(self.background_color)

        background_rect = background_surface.get_rect()
        background_rect.bottomleft = (10, self.screen.get_height() - 10)

        self.screen.blit(background_surface, background_rect)

        input_text_surface = self.font.render(input_text, True, self.text_color)
        input_text_rect = input_text_surface.get_rect(midleft=(background_rect.left + 5, background_rect.centery - 3))
        self.screen.blit(input_text_surface, input_text_rect)
    
class Message:
    def __init__(self, screen):
        self.screen = screen

    def send(self, message: str):
        pass
    
