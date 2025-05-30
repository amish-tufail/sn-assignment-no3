# Main game file - this brings everything together and runs the game loop
# Import all the stuff we need

import pygame
import random
import sys
from game_objects import Player, Enemy, BossEnemy, UpgradeCube, XPTriangle, ShootBoost, PointBoost
from game_utils import (draw_start_screen, draw_game_over_screen, draw_game_ui, 
                         reset_game, get_enemies_needed_for_level, WIDTH, HEIGHT)

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load all images and resize them
bg_image = pygame.image.load('Images/bg.png')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

enemy_image = pygame.image.load('Images/Enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (100, 100))

ship_upgrade_image = pygame.image.load('Images/tank_with_upgrade.png')
ship_upgrade_image = pygame.transform.scale(ship_upgrade_image, (100, 100))

ship_without_upgrade_image = pygame.image.load('Images/tank_without_upgrade.png')
ship_without_upgrade_image = pygame.transform.scale(ship_without_upgrade_image, (100, 100))

upgrade_image = pygame.image.load('Images/Upgrade.png')
upgrade_image = pygame.transform.scale(upgrade_image, (100, 100))

xp_image = pygame.image.load('Images/XP.png')
xp_image = pygame.transform.scale(xp_image, (100, 100))

shoot_boost_image = pygame.image.load('Images/shoot_boost.png')
shoot_boost_image = pygame.transform.scale(shoot_boost_image, (100, 100))

point_boost_image = pygame.image.load('Images/point_boost.png')
point_boost_image = pygame.transform.scale(point_boost_image, (100, 100))

# Load all sounds
gameOver = pygame.mixer.Sound('Sounds/game_over.mp3')
bulletShoot = pygame.mixer.Sound('Sounds/BulletShoot.mp3')
pickUpXpItem = pygame.mixer.Sound('Sounds/pickUpXpItem.mp3')
defetedEnemy = pygame.mixer.Sound('Sounds/defetedEnemy.mp3')
upgradeItemStart = pygame.mixer.Sound('Sounds/upgradeItem.mp3')
XpMinus = pygame.mixer.Sound('Sounds/XpMinus.mp3')
backgroundMusic = pygame.mixer.Sound('Sounds/BackgroundMusic.mp3')
enemyBulletShoot = pygame.mixer.Sound('Sounds/BulletShoot.mp3')

# Set volume levels
background_volume = 0.3
backgroundMusic.set_volume(background_volume)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Current game state
game_state = MENU

# Create all sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boss_enemies = pygame.sprite.Group()
upgrade_cubes = pygame.sprite.Group()
xp_triangles = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
shoot_boosts = pygame.sprite.Group()
point_boosts = pygame.sprite.Group()

# Initialize player as None (will be created when game starts)
player = None

# Start background music
def play_background_music():
    backgroundMusic.play(-1)  # -1 loops forever

# Start the music
play_background_music()

# Game counters and timers
spawn_counter = 0
upgrade_spawn_counter = 0
xp_triangle_spawn_counter = 0
upgrade_spawn_interval = 900  # 15 seconds
xp_triangle_spawn_interval = 900  # 15 seconds

# New collectible spawn timers
shoot_boost_spawn_counter = 0
point_boost_spawn_counter = 0
shoot_boost_spawn_interval = 1200  # 20 seconds
point_boost_spawn_interval = 1500  # 25 seconds

# Level system stuff
current_level = 1
enemies_killed_this_level = 0
boss_spawned = False
level_complete = False

def reset_all_game_variables():
    """Reset all the game counters and variables"""
    global spawn_counter, upgrade_spawn_counter, xp_triangle_spawn_counter
    global current_level, enemies_killed_this_level, boss_spawned, level_complete
    global shoot_boost_spawn_counter, point_boost_spawn_counter
    
    spawn_counter = 0
    upgrade_spawn_counter = 0
    xp_triangle_spawn_counter = 0
    shoot_boost_spawn_counter = 0
    point_boost_spawn_counter = 0
    
    current_level = 1
    enemies_killed_this_level = 0
    boss_spawned = False
    level_complete = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle all events (key presses, mouse clicks, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                    player = reset_game(all_sprites, bullets, enemies, boss_enemies, 
                                      upgrade_cubes, xp_triangles, enemy_bullets, 
                                      shoot_boosts, point_boosts,
                                      ship_without_upgrade_image, ship_upgrade_image)
                    reset_all_game_variables()
            elif game_state == PLAYING:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    game_state = PLAYING
                    player = reset_game(all_sprites, bullets, enemies, boss_enemies, 
                                      upgrade_cubes, xp_triangles, enemy_bullets, 
                                      shoot_boosts, point_boosts,
                                      ship_without_upgrade_image, ship_upgrade_image)
                    reset_all_game_variables()

    # Update game based on current state
    if game_state == PLAYING:
        # Update all sprites
        all_sprites.update()

        # Get how many enemies we need for this level
        enemies_needed_per_level = get_enemies_needed_for_level(current_level)

        # Level progression - spawn enemies for levels 1-3
        if current_level <= 3:
            spawn_counter += 1
            if spawn_counter == 60:  # every second
                enemy = Enemy(enemy_image)
                all_sprites.add(enemy)
                enemies.add(enemy)
                spawn_counter = 0
        elif current_level == 4 and not boss_spawned:
            # spawn boss after level 3
            boss = BossEnemy(enemy_image)
            all_sprites.add(boss)
            boss_enemies.add(boss)
            boss_spawned = True

        # Spawn upgrade cubes
        upgrade_spawn_counter += 1
        if upgrade_spawn_counter == upgrade_spawn_interval:
            upgrade_cube = UpgradeCube(upgrade_image)
            all_sprites.add(upgrade_cube)
            upgrade_cubes.add(upgrade_cube)
            upgrade_spawn_counter = 0

        # Spawn XP triangles
        xp_triangle_spawn_counter += 1
        if xp_triangle_spawn_counter == xp_triangle_spawn_interval:
            xp_triangle = XPTriangle(xp_image)
            all_sprites.add(xp_triangle)
            xp_triangles.add(xp_triangle)
            xp_triangle_spawn_counter = 0

        # Spawn shoot boost
        shoot_boost_spawn_counter += 1
        if shoot_boost_spawn_counter == shoot_boost_spawn_interval:
            shoot_boost = ShootBoost(shoot_boost_image)
            all_sprites.add(shoot_boost)
            shoot_boosts.add(shoot_boost)
            shoot_boost_spawn_counter = 0

        # Spawn point boost
        point_boost_spawn_counter += 1
        if point_boost_spawn_counter == point_boost_spawn_interval:
            point_boost = PointBoost(point_boost_image)
            all_sprites.add(point_boost)
            point_boosts.add(point_boost)
            point_boost_spawn_counter = 0

        # Player picks up upgrade cubes
        upgrade_hits = pygame.sprite.spritecollide(player, upgrade_cubes, True)
        if upgrade_hits:
            player.upgrade()
            upgradeItemStart.play()

        # Player picks up XP triangles (health)
        xp_triangle_hits = pygame.sprite.spritecollide(player, xp_triangles, True)
        for xp_triangle in xp_triangle_hits:
            if player.health < 6:
                player.health += 1
                if player.health > 6:
                    player.health = 6
                pickUpXpItem.play()

        # Player picks up shoot boost
        shoot_boost_hits = pygame.sprite.spritecollide(player, shoot_boosts, True)
        if shoot_boost_hits:
            player.activate_shoot_boost()
            upgradeItemStart.play()

        # Player picks up point boost
        point_boost_hits = pygame.sprite.spritecollide(player, point_boosts, True)
        if point_boost_hits:
            player.score += 10
            pickUpXpItem.play()

        # Player bullets hit enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            player.score += 1
            enemies_killed_this_level += 1
            defetedEnemy.play()
            
            # Check if level is complete
            if enemies_killed_this_level >= enemies_needed_per_level and current_level <= 3:
                current_level += 1
                enemies_killed_this_level = 0
                if current_level > 3:
                    # clear remaining enemies before boss
                    enemies.empty()

        # Player bullets hit boss
        boss_hits = pygame.sprite.groupcollide(boss_enemies, bullets, False, True)
        for boss in boss_hits:
            if boss.hit():  # boss takes damage
                player.score += 10  # bonus points
                boss.kill()
                defetedEnemy.play()
                level_complete = True
                game_state = GAME_OVER

        # Player crashes into enemies
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.health -= 1
                enemy.kill()
                XpMinus.play()
                if player.health <= 0:
                    game_state = GAME_OVER
                    gameOver.play()

        # Player crashes into boss
        for boss in boss_enemies:
            if pygame.sprite.collide_rect(player, boss):
                player.health -= 2  # boss does more damage
                XpMinus.play()
                if player.health <= 0:
                    game_state = GAME_OVER
                    gameOver.play()

        # Enemy bullets hit player
        bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if bullet_hits:
            player.health -= 1
            XpMinus.play()
            if player.health <= 0:
                game_state = GAME_OVER
                gameOver.play()

    # Draw everything based on current state
    if game_state == MENU:
        draw_start_screen(window, bg_image)
    elif game_state == PLAYING:
        # draw background
        window.fill((0, 0, 0))
        window.blit(bg_image, (0, 0))
        
        # draw all sprites
        all_sprites.draw(window)
        
        # draw UI (score, health, etc)
        draw_game_ui(window, player, current_level, enemies_killed_this_level, boss_enemies)
        
    elif game_state == GAME_OVER:
        draw_game_over_screen(window, bg_image, player, level_complete)

    # Update the screen
    pygame.display.flip()
    
    # Keep game running at 60 FPS
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()