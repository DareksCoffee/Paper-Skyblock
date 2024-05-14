from enum import Enum
import pygame

class TileType(Enum):
    
    ## TILES ##
    STONE = pygame.image.load(".\\assets\\textures\\tiles\\stone.png")
    GRASS = pygame.image.load(".\\assets\\textures\\tiles\\grass.png")
    DIRT = pygame.image.load(".\\assets\\textures\\tiles\\dirt.png")
    OAK_LOG = pygame.image.load(".\\assets\\textures\\tiles\\oak_log.png")
    OAK_LEAVE = pygame.image.load(".\\assets\\textures\\tiles\\oak_leave.png")
    OAK_PLANK = pygame.image.load(".\\assets\\textures\\tiles\\oak_planks.png")
    GLASS = pygame.image.load(".\\assets\\textures\\tiles\\glass.png")
    COBBLESTONE = pygame.image.load(".\\assets\\textures\\tiles\\cobblestone.png")

    ## TILES WALL ##
    W_COBBLESTONE = pygame.image.load(".\\assets\\textures\\tiles\\walls\\w_cobblestone.png")
    W_OAK_PLANKS = pygame.image.load(".\\assets\\textures\\tiles\\walls\\w_oak_planks.png")

class Hardness:
    def __init__(self):
        pass

    def getHardness(self, tile_type: TileType) -> float:
        """
        Get tile hardness
        """
        match tile_type:
            case TileType.GRASS:
                return 3
            case TileType.DIRT:
                return 3
            case TileType.STONE:
                return 6
    