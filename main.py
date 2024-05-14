import pygame
import argparse
from paper import Paper
from ext.discord import DiscordWebhook

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
paper = Paper(screen, width, height)
icon = pygame.display.set_icon(pygame.transform.scale(pygame.image.load(".\\assets\\textures\\tiles\\grass.png"), (32, 32)))
discord = DiscordWebhook()

if __name__ == "__main__":
    #discord.send_message("Paper Skyblock has been launched")
    paper.init()