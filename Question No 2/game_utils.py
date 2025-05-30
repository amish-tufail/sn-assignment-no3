# This file has helper functions and screen drawing stuff
# Like the start menu, game over screen, and other useful functions

import pygame

# colors we use in the game
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)

# screen size
WIDTH, HEIGHT = 1000, 700

def get_enemies_needed_for_level(level):
    """tells us how many enemies to kill for each level"""
    if level == 1:
        return 10
    elif level == 2:
        return 20
    elif level == 3:
        return 30
    else:
        return 0  # boss level

def reset_game(all_sprites, bullets, enemies, boss_enemies, upgrade_cubes, 
               xp_triangles, enemy_bullets, shoot_boosts, point_boosts,
               ship_without_upgrade_image, ship_upgrade_image):
    """reset everything when starting new game"""
    from game_objects import Player
    
    # clear all the sprite groups
    all_sprites.empty()
    bullets.empty()
    enemies.empty()
    boss_enemies.empty()
    upgrade_cubes.empty()
    xp_triangles.empty()
    enemy_bullets.empty()
    shoot_boosts.empty()
    point_boosts.empty()
    
    # make new player
    player = Player(ship_without_upgrade_image, ship_upgrade_image)
    all_sprites.add(player)
    
    return player

def draw_start_screen(window, bg_image):
    """draw the main menu screen"""
    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))
    
    # fonts for different text sizes
    title_font = pygame.font.Font(None, 72)
    subtitle_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)
    instruction_font = pygame.font.Font(None, 24)
    
    # main title
    title_text = title_font.render("SIDE SCROLLING", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(title_text, title_rect)
    
    # subtitle
    subtitle_text = subtitle_font.render("2D GAME", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(subtitle_text, subtitle_rect)
    
    # start instruction
    start_text = text_font.render("PRESS SPACE TO START THE GAME", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    window.blit(start_text, start_rect)
    
    # instructions in corner
    instructions_title = instruction_font.render("INSTRUCTIONS:", True, WHITE)
    window.blit(instructions_title, (WIDTH - 250, 20))
    
    # control instructions
    instructions = [
        "SPACE - Shoot",
        "W - Move Up",
        "S - Move Down", 
        "A - Move Left",
        "D - Move Right",
        "",
        "Collect upgrades and XP!",
        "Survive 3 levels + Boss!"
    ]
    
    y_offset = 50
    for instruction in instructions:
        if instruction == "":  # empty line for spacing
            y_offset += 10
            continue
        instr_text = instruction_font.render(instruction, True, WHITE)
        window.blit(instr_text, (WIDTH - 250, y_offset))
        y_offset += 25

def draw_game_over_screen(window, bg_image, player, won=False):
    """draw the game over screen"""
    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))
    
    title_font = pygame.font.Font(None, 72)
    subtitle_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 36)
    
    if won:
        # win text
        win_text = title_font.render("YOU WIN!", True, GREEN)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(win_text, win_rect)
        
        boss_text = subtitle_font.render("BOSS DEFEATED!", True, GREEN)
        boss_rect = boss_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        window.blit(boss_text, boss_rect)
    else:
        # game over text
        game_over_text = title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        window.blit(game_over_text, game_over_rect)
    
    # final score
    score_text = subtitle_font.render(f"FINAL SCORE: {player.score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    window.blit(score_text, score_rect)
    
    # restart instruction
    restart_text = text_font.render("PRESS 'R' TO PLAY AGAIN", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    window.blit(restart_text, restart_rect)

def draw_game_ui(window, player, current_level, enemies_killed_this_level, boss_enemies):
    """draw all the game UI like score, health bar etc"""
    text_font = pygame.font.Font(None, 36)
    
    # score
    score_text = text_font.render(f"Score: {player.score}", True, WHITE)
    window.blit(score_text, (WIDTH - 150, 10))

    # level info
    if current_level <= 3:
        level_text = text_font.render(f"Level: {current_level}", True, WHITE)
        window.blit(level_text, (WIDTH - 150, 50))
        enemies_needed = get_enemies_needed_for_level(current_level)
        progress_text = text_font.render(f"Enemies: {enemies_killed_this_level}/{enemies_needed}", True, WHITE)
        window.blit(progress_text, (WIDTH - 200, 90))
    elif current_level == 4:
        boss_text = text_font.render("BOSS FIGHT!", True, RED)
        window.blit(boss_text, (WIDTH - 150, 50))
        # show boss health if boss exists
        for boss in boss_enemies:
            boss_health_text = text_font.render(f"Boss HP: {boss.health}/{boss.max_health}", True, RED)
            window.blit(boss_health_text, (WIDTH - 180, 90))

    # health bar
    pygame.draw.rect(window, GRAY, (10, 10, 200, 30))
    health_width = player.health * 33.33
    if player.health >= 4:
        color = GREEN
    elif player.health >= 2:
        color = ORANGE
    else:
        color = RED
    pygame.draw.rect(window, color, (10, 10, health_width, 30))

    # health number
    hx_text = text_font.render(f"HX: {player.health}", True, WHITE)
    window.blit(hx_text, (220, 10))

    # upgrade timer
    if player.upgraded:
        upgrade_timer_text = text_font.render(f"Upgrade: {15 - player.upgrade_timer // 60}", True, WHITE)
        window.blit(upgrade_timer_text, (10, 50))

    # shoot boost timer
    if player.shoot_boost_active:
        shoot_boost_timer_text = text_font.render(f"Auto Shoot: {10 - player.shoot_boost_timer // 60}", True, BLUE)
        window.blit(shoot_boost_timer_text, (10, 90))