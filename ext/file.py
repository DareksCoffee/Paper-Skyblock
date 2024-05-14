import os
import random

class Save:
    def __init__(self):
        self.saves = 9

    def world(self, world_tiles):
        print("saving.")
        """Save world"""
        path = f"saves\map0.2dsky"
        if not os.path.exists(path):
            with open(path, "w") as file:
                for (x, y), tile_type in world_tiles:
                    file.write(f"{x},{y},{tile_type}\n")
class Load:
    def __init__(self):
        pass

    def world(self):
        """Load World"""