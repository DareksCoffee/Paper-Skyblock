import pygame

class Collision:
    def __init__(self):
        pass

    def isColliding(self, rect1, rect2):
        """Check if two rectangles are colliding."""
        return rect1.colliderect(rect2)