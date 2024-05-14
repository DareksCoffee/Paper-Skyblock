import pygame
from tiles.tile import Tile
from tiles.tiletype import TileType
from utils.screen import Screen

class World:
    def __init__(self, screen, width: int, height: int):
        self.screen = screen
        self.width = width
        self.height = height
        self.mouse_pos = pygame.mouse.get_pos()
        self.hasGenerated = False
        self.tile = Tile(self.screen, self.width, self.height)
        self.utils = Screen(self.screen, self.width, self.height)

    def generateTree(self, x, y) -> None:
        tile_spacing = 2 * 16
        for k in range(4):
            self.tile.placeTile(TileType.OAK_LOG, x, y - tile_spacing - (k * 32) + 1)

        for l in range(3): 
            for m in range(-2, 3):
                self.tile.placeTile(TileType.OAK_LEAVE, x + (m * tile_spacing), y - tile_spacing - (k * 31) - (l * tile_spacing)) 

    def generate(self) -> None:
        """
        Generate a Skyblock World.
        """

        middle_x, middle_y = self.utils.getResCenter()
            
        rows = 3
        columns = 9
        grid_size = 32

        # Calculate the starting position of the grid
        start_x = middle_x - (self.tile.tile_scale * self.tile.tile_size) - 44
        start_y = middle_y - (self.tile.tile_scale * self.tile.tile_size) - 44

        for i in range(rows):
            for j in range(columns):
                x = start_x + j * grid_size
                y = start_y + i * grid_size
                
                if i >= 1:
                    self.tile.placeTile(TileType.DIRT, x, y)
                else:
                    tile_type = TileType.GRASS
                    if j == 6: 
                        self.generateTree(x, y)
                    self.tile.placeTile(tile_type, x, y)

        self.tile.renderTiles()

        self.hasGenerated = True

        def _hasGenerated(self) -> bool:
            return self.hasGenerated