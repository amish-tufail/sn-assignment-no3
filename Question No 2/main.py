import pygame
import sys
from screens.start_screen import show_start_screen

pygame.init()
pygame.mixer.init() 

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroll")

show_start_screen(screen, WIDTH, HEIGHT)

print("Continue to next screen...")
