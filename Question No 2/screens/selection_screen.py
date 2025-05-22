import pygame
import sys

def show_tank_selection_screen(screen, width, height):
    # Set the background color to yellow
    screen.fill((255, 255, 0))

    # Load tank images from the assets folder
    tank1_image = pygame.image.load("assets/tank1.png")
    tank2_image = pygame.image.load("assets/tank2.png")
    tank3_image = pygame.image.load("assets/tank3.png")
    tank4_image = pygame.image.load("assets/tank4.png")
    
    # Resize the tank images to a smaller size
    tank1_image = pygame.transform.scale(tank1_image, (75, 75))  # Smaller size for tank images
    tank2_image = pygame.transform.scale(tank2_image, (75, 75))  # Smaller size for tank images
    tank3_image = pygame.transform.scale(tank3_image, (75, 75))  # Smaller size for tank images
    tank4_image = pygame.transform.scale(tank4_image, (75, 75))  # Smaller size for tank images
    
    # Fonts for text and descriptions
    title_font = pygame.font.SysFont(None, 40)  # Font for instructions title
    description_font = pygame.font.SysFont(None, 24)  # Font for description text

    # Text for the title
    title_text = title_font.render("Choose Your Tank", True, (0, 0, 0))

    # Descriptions for Tank 1, Tank 2, Tank 3, and Tank 4
    tank1_desc = description_font.render("Tank 1: Fast and Agile", True, (0, 0, 0))
    tank2_desc = description_font.render("Tank 2: Heavy and Powerful", True, (0, 0, 0))
    tank3_desc = description_font.render("Tank 3: Balanced and Steady", True, (0, 0, 0))
    tank4_desc = description_font.render("Tank 4: Quick and Versatile", True, (0, 0, 0))

    # Positioning of elements
    title_rect = title_text.get_rect(center=(width // 2, 50))  # Title centered at top

    # Positioning for Tank 1 and its description (centered with description to the right)
    tank1_rect = tank1_image.get_rect(center=(width // 2, height // 3))  # Increased spacing from the title
    tank1_desc_rect = tank1_desc.get_rect(left=(width // 2 + 80), centery=(height // 3))  # Left-aligned description

    # Positioning for Tank 2 and its description (centered with description to the right)
    tank2_rect = tank2_image.get_rect(center=(width // 2, height // 2))
    tank2_desc_rect = tank2_desc.get_rect(left=(width // 2 + 80), centery=(height // 2))  # Left-aligned description

    # Positioning for Tank 3 and its description (centered with description to the right)
    tank3_rect = tank3_image.get_rect(center=(width // 2, height // 1.5))
    tank3_desc_rect = tank3_desc.get_rect(left=(width // 2 + 80), centery=(height // 1.5))  # Left-aligned description

    # Positioning for Tank 4 and its description (centered with description to the right)
    tank4_rect = tank4_image.get_rect(center=(width // 2, height // 1.2))
    tank4_desc_rect = tank4_desc.get_rect(left=(width // 2 + 80), centery=(height // 1.2))  # Left-aligned description

    # Selection indicator (an arrow pointing to the left of the selected tank)
    def draw_arrow(x, y):
        # Draw an arrow pointing to the left of the selected tank
        points = [(x, y), (x - 10, y - 5), (x - 10, y + 5)]  # Arrow points
        pygame.draw.polygon(screen, (0, 0, 0), points)  # Black arrow

    # For keeping track of the selected tank (1 to 4)
    selected_tank = 1

    waiting = True
    while waiting:
        # Fill the screen with yellow
        screen.fill((255, 255, 0))

        # Draw the title
        screen.blit(title_text, title_rect)
        
        # Draw Tanks and descriptions
        screen.blit(tank1_image, tank1_rect)
        screen.blit(tank1_desc, tank1_desc_rect)
        
        screen.blit(tank2_image, tank2_rect)
        screen.blit(tank2_desc, tank2_desc_rect)
        
        screen.blit(tank3_image, tank3_rect)
        screen.blit(tank3_desc, tank3_desc_rect)
        
        screen.blit(tank4_image, tank4_rect)
        screen.blit(tank4_desc, tank4_desc_rect)

        # Draw the selection arrow for the selected tank
        if selected_tank == 1:
            draw_arrow(tank1_rect.left - 20, tank1_rect.centery)
        elif selected_tank == 2:
            draw_arrow(tank2_rect.left - 20, tank2_rect.centery)
        elif selected_tank == 3:
            draw_arrow(tank3_rect.left - 20, tank3_rect.centery)
        elif selected_tank == 4:
            draw_arrow(tank4_rect.left - 20, tank4_rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Move selection to the tank above (if we're not already on the first tank)
                    if selected_tank > 1:
                        selected_tank -= 1
                elif event.key == pygame.K_DOWN:
                    # Move selection to the tank below (if we're not already on the last tank)
                    if selected_tank < 4:
                        selected_tank += 1
                elif event.key == pygame.K_SPACE:
                    # Proceed to the next screen when Space is pressed
                    waiting = False
                    print(f"Tank {selected_tank} selected!")
                    # Here, you can transition to your next screen or game
                    # For example: game_loop(selected_tank)

    pygame.mixer.music.stop()
