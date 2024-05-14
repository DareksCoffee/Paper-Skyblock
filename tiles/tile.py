import pygame
from tiles.tiletype import TileType
from tiles.tiles import TILES, TILE_RECTS
import numpy as np
import pygame.surfarray as surfarray

class Tile:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.tile_scale = 2
        self.tile_size = 2
        self.scaled_textures = {}
        
        for tile_type in TileType:
            scaled_image = pygame.transform.scale(tile_type.value, 
                                                  (tile_type.value.get_width() * self.tile_scale, 
                                                   tile_type.value.get_height() * self.tile_scale))
            self.scaled_textures[tile_type] = scaled_image

    def getTileMap(self) -> dict:
        return TILES
    
    def placeTile(self, tile_type: TileType, x: float, y: float) -> None:
        """Place a tile at the given position."""

        x_pos, y_pos = int(x), int(y)
        if (x_pos, y_pos) not in TILES:
            TILES[(x_pos, y_pos)] = tile_type

    def destroyTile(self, x: float, y: float) -> None:
        """Destroy a tile at the given position."""
        x_pos, y_pos = int(x), int(y)
        if (x_pos, y_pos) in TILES:
            del TILES[(x_pos, y_pos)]
            if (x_pos, y_pos) in TILE_RECTS:
                del TILE_RECTS[(x_pos, y_pos)] 


    def renderTiles(self) -> None:
        """Render all tiles onto the screen and generate tile rects."""
        
        sorted_tiles = sorted(TILES.items(), key=lambda item: item[0][1]) 
        
        for (x, y), tile_type in sorted_tiles:
            x_pos, y_pos = int(x), int(y)
            texture = self.scaled_textures[tile_type]
            rect = pygame.Rect(x_pos, y_pos, texture.get_width(), texture.get_height())

            num_tiles_above = sum(1 for dy in range(1, 4) if (x_pos, y_pos - dy * 32) in TILES)
            match num_tiles_above:
                case 0:
                    darken_factor = 0.4
                case 1:
                    darken_factor = 0.3
                case 2:
                    darken_factor = 0.2
                case _:
                    darken_factor = 0.1

            if (x_pos, y_pos - 32) in TILES and TILES[(x_pos, y_pos)] != TileType.OAK_LEAVE:
                texture = self.darkenTexture(texture, darken_factor)

            if (x_pos, y_pos) not in TILE_RECTS:
                TILE_RECTS[(x_pos, y_pos)] = rect

            self.screen.blit(texture, (x_pos, y_pos))

    def darkenTexture(self, texture: pygame.Surface, darken_factor: float) -> pygame.Surface:
        """Darken a texture by multiplying its color components by a given factor."""
        texture_array = surfarray.array3d(texture)
        texture_array[:, :, :3] = (texture_array[:, :, :3] * darken_factor).astype(np.uint8)

        darkened_texture = surfarray.make_surface(texture_array)
        return darkened_texture

    def calculateTiles(self, x: float, y: float, player_x: float, player_y: float) -> float:
        """Calculate the number of tiles between a given position and the player's position."""
        tile_scale = self.tile_scale * 16
        distance_x = abs(x - player_x)
        distance_y = abs(y - player_y)

        tiles_x = distance_x / tile_scale
        tiles_y = distance_y / tile_scale

        return tiles_x, tiles_y

    def getType(self, x: float, y: float):
        if(int(x), int(y)) in TILES:
            tile_type = TILES[(x, y)]
            return tile_type

    def getTileRects(self) -> dict:
        """Return the dictionary of tile rects."""
        return TILE_RECTS