import pygame
import sys

def show_start_screen(screen, width, height):

    pygame.mixer.music.load("assets/menu_song.ogg")  
    pygame.mixer.music.play(-1) 

    title_font = pygame.font.SysFont(None, 80)
    info_font = pygame.font.SysFont(None, 36)

    title_text = title_font.render("Side Scrolling", True, (255, 255, 255))
    info_text = info_font.render("Press any key to continue", True, (200, 200, 200))

    title_rect = title_text.get_rect(center=(width // 2, height // 2))
    info_rect = info_text.get_rect(center=(width // 2, height - 50))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0)) 

        screen.blit(title_text, title_rect)
        screen.blit(info_text, info_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False 

    pygame.mixer.music.stop() 
