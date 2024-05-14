import pygame

class Pause:
    """Pause menu"""

    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        """Draw pause menu"""

        rect = pygame.draw.rect(self.screen, self.screen.get_width())
