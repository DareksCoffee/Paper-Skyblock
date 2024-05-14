import pygame
from tiles.tiletype import TileType

class Durability:
    def __init__(self):
        self.durability = 0

    def remDurability(self, tiletype: TileType) -> float:
        durability = 0
        match tiletype:
            case TileType.GRASS:
                return 0
            