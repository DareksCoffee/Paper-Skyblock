import pygame
import platform
import wmi  
from pygame.locals import *
from gui.text import Text
from tiles.tile import Tile
from ext.player import Player

class Debug:
    def __init__(self, screen, width, height, version, clock, player):
        self.screen = screen
        self.width = width
        self.height = height
        self.version = version
        self.clock = clock
        self.player = player
        self.text = Text()
        self.tile = Tile(self.screen, self.width, self.height)
        self.font = self.text.text_font
            

        self.text_color = (255, 255, 255)
        self.background_color = (50, 50, 50, 125)
        
    def renderText(self, text, font, position):

        text_surface = font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(topleft=position)
        background_surface = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
        background_surface.fill(self.background_color)
        self.screen.blit(background_surface, text_rect)
        self.screen.blit(text_surface, text_rect)
        return text_rect  

    def display(self) -> None:
        text = Text()
        fps = self.clock.get_fps()
        mouse = pygame.mouse.get_pos()

        title_text = f"PaperCraft {self.version} ({self.version}/vanilla)"
        fps_text = f"{int(fps)} fps"
        tiles_num = f"{len(self.tile.getTileMap())} tiles rendered"
        position = f"XY: {self.player.x_pos:.2f} / {self.player.y_pos:.2f}"
        mouse_title = "Mouse Informations"
        mouse_pos = f"Mouse XY: {mouse[0]} / {mouse[1]}"

        self.renderText(title_text, self.font, (10, 0))
        self.renderText(fps_text, self.font, (10, 20))
        self.renderText(tiles_num, self.font, (10, 40))
        self.renderText(position, self.font, (10, 80))
        self.renderText(mouse_title, self.font, (650, 0))
        self.renderText(mouse_pos, self.font, (650, 20))


        self.clock.tick(120)