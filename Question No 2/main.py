import pygame
import sys
from screens.start_screen import show_start_screen
from screens.instruction_screen import show_instructions_screen
from screens.selection_screen import show_tank_selection_screen  # Import tank selection screen


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroll")

# Show start screen first
show_start_screen(screen, WIDTH, HEIGHT)

# After pressing any key, show instructions screen
show_instructions_screen(screen, WIDTH, HEIGHT)

# After instructions, show tank selection screen
show_tank_selection_screen(screen, WIDTH, HEIGHT)

print("Continue to next screen...")

