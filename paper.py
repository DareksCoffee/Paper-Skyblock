import pygame
import numpy as np
from pygame.locals import *
from world.environment import Background, Clouds, Sun
from world.gen import World
from gui.debug import Debug
from gui.chat import InputBox
from tiles.tile import Tile
from tiles.tiletype import TileType, Hardness
from tiles.tiles import TILES, TILE_RECTS
from ext.player import Player
from ext.discord import DiscordWebhook
from ext.file import Save, Load

class Paper:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.version = "0.20a"

        self.tile = Tile(self.screen, self.width, self.height)

        self.x_pos = 350
        self.y_pos = 300

        self.player = Player(self.x_pos, self.y_pos, self.screen)
        self.world = World(self.screen, self.width, self.height)
        self.save = Save()
        self.hardness = Hardness()
        self.debug_visible = False 
        self.selected_tile = TileType.GRASS

        self.cloud_images = [pygame.image.load(f".\\assets\\textures\\environment\\clouds\\cloud{i}.png").convert_alpha() for i in range(4)]
        self.clouds = Clouds(self.screen, self.cloud_images, self.width, self.height)

        self.inputBox = InputBox(self.screen)
        self.inputVisible = False

    def init(self) -> None:
        clock = pygame.time.Clock()
        background = Background(self.screen, self.width, self.height)
        debug = Debug(self.screen, self.width, self.height, self.version, pygame.time.Clock(), self.player)
        sun = Sun(self.screen)
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        self.debug_visible = not self.debug_visible
                    elif event.key == pygame.K_t:
                        self.inputVisible = not self.inputVisible
                    elif event.key == pygame.K_1:
                        self.selected_tile = TileType.GRASS
                    elif event.key == pygame.K_2:
                        self.selected_tile = TileType.DIRT
                    elif event.key == pygame.K_3:
                        self.selected_tile = TileType.STONE
                    elif event.key == pygame.K_4:
                        self.selected_tile = TileType.OAK_LOG
                    elif event.key == pygame.K_5:
                        self.selected_tile = TileType.OAK_LEAVE
                    elif event.key == pygame.K_6:
                        self.selected_tile = TileType.OAK_PLANK
                    elif event.key == pygame.K_7:
                        self.selected_tile = TileType.COBBLESTONE
                    elif event.key == pygame.K_8:
                        self.selected_tile = TileType.GLASS
                    elif event.key == pygame.K_9:
                        self.selected_tile = TileType.W_COBBLESTONE
                    elif event.key == pygame.K_0:
                        self.selected_tile = TileType.W_OAK_PLANKS
          
                    else:
                        self.player.handleKeyPress(event) 
                elif event.type == pygame.KEYUP:
                    self.player.handleKeyRelease(event) 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.player.punch()
                        mouse_pos = pygame.mouse.get_pos()
                        #distance_to_player = self.tile.calculateTiles(x_pos, y_pos, self.player.x_pos, self.player.y_pos)
                        self.player.placeTile(self.selected_tile, mouse_pos)

                    elif event.button == 1:
                        self.player.punch()
                        mouse_pos = pygame.mouse.get_pos()
                        #distance_to_player = self.tile.calculateTiles(x_pos, y_pos, self.player.x_pos, self.player.y_pos)
                        self.player.destroyTile(mouse_pos)

            title = pygame.display.set_caption("PaperCraft")
            tiles = TILE_RECTS
            self.screen.fill(background.getColor())
            
            #sun.draw()
            #sun.update()

            self.player.getPlyrName()
            if self.inputVisible:
                self.inputBox.displayInput("hello this is a test")

            ## Background ##
            self.clouds.update()
            #################

            ## World ##
            if not self.world.hasGenerated:
                self.world.generate()
            self.tile.renderTiles()
            ######################

            ## Player ##
            self.player.updateGravity()
            self.player.draw()
            self.player.handle_input()
            self.player.update_punch()
            self.player.update_leg()
            self.player.checkCollision(TILE_RECTS)
            #######################

            if self.debug_visible:
                debug.display()

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()