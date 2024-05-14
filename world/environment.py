import pygame
import math
import random

class Background:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.bgColor = (148, 151, 255)
    
    def getColor(self) -> tuple:
        return self.bgColor

class Clouds:
    def __init__(self, screen, cloud_images, width, height):
        self.screen = screen
        self.cloud_images = cloud_images
        self.width = width
        self.height = height
        self.clouds = []
        self.max_clouds = 2  # Maximum number of clouds to spawn
        self.spawn_chance = 0.1  # Chance of spawning a cloud
        self.cloud_speed = 0.3

    def spawn_cloud(self):
        """Spawn clouds to screen."""
        if len(self.clouds) < self.max_clouds and random.random() < self.spawn_chance:
            cloud_image = random.choice(self.cloud_images)
            cloud_size = random.uniform(1.5, 5)  
            cloud_image = pygame.transform.scale(cloud_image, (int(cloud_image.get_width() * cloud_size), int(cloud_image.get_height() * cloud_size)))
            cloud_rect = cloud_image.get_rect()
            cloud_rect.left = -cloud_rect.width
            cloud_rect.top = random.randint(100, 300)
            self.clouds.append((cloud_image, cloud_rect))

    def move_clouds(self):
        """Move the clouds towards the right."""
        for cloud, rect in self.clouds:
            rect.move_ip(self.cloud_speed, 0)

    def draw(self):
        """Draw the clouds on the screen."""
        for cloud, rect in self.clouds:
            self.screen.blit(cloud, rect)

    def update(self):
        """Update the cloud movement."""
        self.spawn_cloud()
        self.move_clouds()
        self.draw()


class Sun:
    def __init__(self, screen):
        self.screen = screen
        self.sun = pygame.image.load("assets\\textures\\environment\\sun.png").convert_alpha()
        self.sun = pygame.transform.scale(self.sun, (64, 64))  
        self.start_pos = (800, 0)  
        self.end_pos = (0, 800)    
        self.time_passed = 0         

    def draw(self):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * 0.5 * (1 + math.cos(self.time_passed * 0.005))
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * 0.5 * (1 - math.sin(self.time_passed * 0.005))

        self.screen.blit(self.sun, (x, y))
        
    def update(self):
        self.time_passed += 0.05