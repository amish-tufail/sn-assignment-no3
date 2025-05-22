import pygame
import sys

def show_instructions_screen(screen, width, height):
    background = pygame.image.load("assets/menu_background.png")
    background = pygame.transform.scale(background, (width, height))
    
    pygame.mixer.music.load("assets/menu_song.ogg")  
    pygame.mixer.music.play(-1)

    # Fonts
    title_font = pygame.font.SysFont(None, 40)  # Font for instructions title
    info_font = pygame.font.SysFont(None, 30)   # Font for "Press SPACE"
    instructions_font = pygame.font.SysFont(None, 24)  # Smaller font size for instructions

    # Text for "Press SPACE to play"
    info_text = info_font.render("Press SPACE to play", True, (200, 200, 200))

    # Text for instructions title
    instructions_title_text = title_font.render("Instructions:", True, (200, 255, 255))

    # Text for individual instructions
    instruction1 = instructions_font.render("Press UP to move up", True, (255, 255, 255))
    instruction2 = instructions_font.render("Press DOWN to move down", True, (255, 255, 255))
    instruction3 = instructions_font.render("Press LEFT to move left", True, (255, 255, 255))
    instruction4 = instructions_font.render("Press RIGHT to move right", True, (255, 255, 255))
    instruction5 = instructions_font.render("Press SPACE to shoot", True, (255, 255, 255))

    # Positioning the elements
    # Center "Press SPACE" at the bottom of the screen
    info_rect = info_text.get_rect(center=(width // 2, height - 30))

    # Instructions title at the top left
    instructions_title_rect = instructions_title_text.get_rect(center=(width // 4, height // 2))

    # Positioning each instruction centered on the left side of the screen
    instruction1_rect = instruction1.get_rect(center=(width // 2, height // 2 - 60))
    instruction2_rect = instruction2.get_rect(center=(width // 2, height // 2 - 30))
    instruction3_rect = instruction3.get_rect(center=(width // 2, height // 2))
    instruction4_rect = instruction4.get_rect(center=(width // 2, height // 2 + 30))
    instruction5_rect = instruction5.get_rect(center=(width // 2, height // 2 + 60))

    waiting = True
    while waiting:
        screen.blit(background, (0, 0))

        # Draw instructions title and each individual instruction
        screen.blit(instructions_title_text, instructions_title_rect)
        screen.blit(instruction1, instruction1_rect)
        screen.blit(instruction2, instruction2_rect)
        screen.blit(instruction3, instruction3_rect)
        screen.blit(instruction4, instruction4_rect)
        screen.blit(instruction5, instruction5_rect)

        # Draw "Press SPACE to play" text at the bottom center
        screen.blit(info_text, info_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Start the game when Space is pressed

    pygame.mixer.music.stop()
