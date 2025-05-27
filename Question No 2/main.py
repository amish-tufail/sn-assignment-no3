import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1000, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)

# Load PNG images and resize them
bg_image = pygame.image.load('Images/bg.png')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

enemy_image = pygame.image.load('Images/Enemy.png')
enemy_image = pygame.transform.scale(enemy_image, (100, 100))  # Adjust size as needed

ship_upgrade_image = pygame.image.load('Images/tank_with_upgrade.png')
ship_upgrade_image = pygame.transform.scale(ship_upgrade_image, (100, 100))  # Adjust size as needed

ship_without_upgrade_image = pygame.image.load('Images/tank_without_upgrade.png')
ship_without_upgrade_image = pygame.transform.scale(ship_without_upgrade_image, (100, 100))  # Adjust size as needed

upgrade_image = pygame.image.load('Images/Upgrade.png')
upgrade_image = pygame.transform.scale(upgrade_image, (100, 100))  # Adjust size as needed

xp_image = pygame.image.load('Images/XP.png')
xp_image = pygame.transform.scale(xp_image, (100, 100))  # Adjust size as needed

# Load new collectible images
shoot_boost_image = pygame.image.load('Images/shoot_boost.png')
shoot_boost_image = pygame.transform.scale(shoot_boost_image, (100, 100))

point_boost_image = pygame.image.load('Images/point_boost.png')
point_boost_image = pygame.transform.scale(point_boost_image, (100, 100))

# Sounds
gameOver = pygame.mixer.Sound('Sounds/game_over.mp3')
bulletShoot = pygame.mixer.Sound('Sounds/BulletShoot.mp3')
pickUpXpItem = pygame.mixer.Sound('Sounds/pickUpXpItem.mp3')
defetedEnemy = pygame.mixer.Sound('Sounds/defetedEnemy.mp3')
upgradeItemStart = pygame.mixer.Sound('Sounds/upgradeItem.mp3')
XpMinus = pygame.mixer.Sound('Sounds/XpMinus.mp3')
backgroundMusic = pygame.mixer.Sound('Sounds/BackgroundMusic.mp3')
enemyBulletShoot = pygame.mixer.Sound('Sounds/BulletShoot.mp3')  # Define enemy bullet shooting sound

# Set initial volume levels
volume_once = 0.8  # Example volume level for "once" sound
volume_sometimes = 0.5  # Example volume level for "sometimes" sound
background_volume = 0.3  # Adjust background music volume here

# Set volume for background music
backgroundMusic.set_volume(background_volume)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Current game state
game_state = MENU

# Set up fonts
title_font = pygame.font.Font(None, 72)
subtitle_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 36)

# Function to play sounds
def play_sound(sound):
    sound.play()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = ship_without_upgrade_image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.left = 10  # Position player on the left side
        self.rect.centery = HEIGHT // 2  # Center vertically
        self.speed = 5
        self.double_shooter = False
        self.upgraded = False
        self.upgrade_timer = 0
        self.score = 0
        self.health = 6
        
        # New shoot boost properties
        self.shoot_boost_active = False
        self.shoot_boost_timer = 0
        self.auto_shoot_counter = 0

    def update(self):
        keys = pygame.key.get_pressed()
        # Move up and down
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        # Move forward and backward (left-right)
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.clamp_ip(window.get_rect())

        # Check if player is upgraded
        if self.upgraded:
            self.upgrade_timer += 1
            if self.upgrade_timer >= 900:  # 15 seconds (60 frames per second * 15)
                self.downgrade()
        
        # Check if shoot boost is active
        if self.shoot_boost_active:
            self.shoot_boost_timer += 1
            self.auto_shoot_counter += 1
            
            # Auto shoot every 10 frames (6 times per second)
            if self.auto_shoot_counter >= 10:
                self.shoot()
                self.auto_shoot_counter = 0
            
            # End shoot boost after 10 seconds
            if self.shoot_boost_timer >= 600:  # 10 seconds (60 frames per second * 10)
                self.shoot_boost_active = False
                self.shoot_boost_timer = 0
        
        # Update speed if player is upgraded
        if self.upgraded:
            self.speed = 8  # Increase speed when upgraded
        else:
            self.speed = 5  # Reset speed if not upgraded

    def upgrade(self):
        self.upgraded = True
        self.original_image = ship_upgrade_image
        self.image = self.original_image.copy()
        self.double_shooter = True
        self.upgrade_timer = 0

    def downgrade(self):
        self.upgraded = False
        self.original_image = ship_without_upgrade_image
        self.image = self.original_image.copy()
        self.double_shooter = False

    def activate_shoot_boost(self):
        self.shoot_boost_active = True
        self.shoot_boost_timer = 0
        self.auto_shoot_counter = 0

    def shoot(self):
        if self.double_shooter:  # Double shoot when upgraded
            bullet1 = Bullet(self.rect.right, self.rect.top)
            bullet2 = Bullet(self.rect.right, self.rect.bottom)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
        else:
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
        play_sound(bulletShoot)  # Play shooting sound

# Define the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10  # Move to the right

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Define the enemy bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)  # Color of the enemy bullet
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speed = -5  # Move to the left (towards player)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

# Define the enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(1, 2)
        self.shoot_probability = 0.01  # Adjust this probability as needed

    def update(self):
        self.rect.x -= self.speed  # Move to the left
        if self.rect.right < 0:  # If enemy passes the left edge
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.randint(1, 2)
            play_sound(XpMinus)  # Play XP minus sound

        # Randomly decide whether to shoot
        if random.random() <= self.shoot_probability:
            self.shoot()

    def shoot(self):
        # Create a bullet shot by the enemy
        bullet = EnemyBullet(self.rect.left, self.rect.centery)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        play_sound(enemyBulletShoot)  # Play shooting sound

class UpgradeCube(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = upgrade_image  # Use the loaded Upgrade.png image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(4, 6)  # Increase speed to make it harder to get upgrades

    def update(self):
        self.rect.x -= self.speed  # Move to the left
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.randint(4, 6)  # Randomize speed to add variability in movement

# New Shoot Boost collectible class
class ShootBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = shoot_boost_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed  # Move to the left
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.randint(3, 5)

# New Point Boost collectible class
class PointBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = point_boost_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed  # Move to the left
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.randint(3, 5)

# Define the boss enemy class
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Make boss 1.5x larger
        boss_size = (150, 150)
        self.image = pygame.transform.scale(enemy_image, boss_size)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.centery = HEIGHT // 2  # Center vertically
        self.speed = 1  # Slower than regular enemies
        self.health = 10  # Takes more hits to destroy
        self.max_health = 10
        self.shoot_probability = 0.05  # Higher shooting rate

    def update(self):
        self.rect.x -= self.speed  # Move to the left slowly
        # Keep boss on screen, don't let it go past left edge
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.centery = HEIGHT // 2

        # Higher chance to shoot
        if random.random() <= self.shoot_probability:
            self.shoot()

    def shoot(self):
        # Boss shoots multiple bullets
        bullet1 = EnemyBullet(self.rect.left, self.rect.top + 30)
        bullet2 = EnemyBullet(self.rect.left, self.rect.centery)
        bullet3 = EnemyBullet(self.rect.left, self.rect.bottom - 30)
        all_sprites.add(bullet1, bullet2, bullet3)
        enemy_bullets.add(bullet1, bullet2, bullet3)
        play_sound(enemyBulletShoot)

    def hit(self):
        self.health -= 1
        return self.health <= 0  # Returns True if boss is defeated

class XPTriangle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = xp_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH  # Start from the right side
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed  # Move to the left
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.randint(1, 3)

def get_enemies_needed_for_level(level):
    """Return the number of enemies needed for each level"""
    if level == 1:
        return 10
    elif level == 2:
        return 20
    elif level == 3:
        return 30
    else:
        return 0  # Boss level

def reset_game():
    """Reset all game variables to initial state"""
    global player, spawn_counter, upgrade_spawn_counter, xp_triangle_spawn_counter
    global current_level, enemies_killed_this_level, boss_spawned, level_complete
    global shoot_boost_spawn_counter, point_boost_spawn_counter
    
    # Clear all sprite groups
    all_sprites.empty()
    bullets.empty()
    enemies.empty()
    boss_enemies.empty()
    upgrade_cubes.empty()
    xp_triangles.empty()
    enemy_bullets.empty()
    shoot_boosts.empty()
    point_boosts.empty()
    
    # Create new player
    player = Player()
    all_sprites.add(player)
    
    # Reset counters
    spawn_counter = 0
    upgrade_spawn_counter = 0
    xp_triangle_spawn_counter = 0
    shoot_boost_spawn_counter = 0
    point_boost_spawn_counter = 0
    
    # Reset level system
    current_level = 1
    enemies_killed_this_level = 0
    boss_spawned = False
    level_complete = False

def draw_start_screen():
    """Draw the start screen"""
    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))  # Draw background image
    
    # Main title
    title_text = title_font.render("SIDE SCROLLING", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(title_text, title_rect)
    
    # Subtitle
    subtitle_text = subtitle_font.render("2D GAME", True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(subtitle_text, subtitle_rect)
    
    # Start instruction
    start_text = text_font.render("PRESS SPACE TO START THE GAME", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    window.blit(start_text, start_rect)

def draw_game_over_screen(won=False):
    """Draw the game over screen"""
    window.fill((0, 0, 0))
    window.blit(bg_image, (0, 0))  # Draw background image
    
    if won:
        # Win text
        win_text = title_font.render("YOU WIN!", True, GREEN)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(win_text, win_rect)
        
        boss_text = subtitle_font.render("BOSS DEFEATED!", True, GREEN)
        boss_rect = boss_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        window.blit(boss_text, boss_rect)
    else:
        # Game over text
        game_over_text = title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        window.blit(game_over_text, game_over_rect)
    
    # Final score
    score_text = subtitle_font.render(f"FINAL SCORE: {player.score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    window.blit(score_text, score_rect)
    
    # Restart instruction
    restart_text = text_font.render("PRESS 'R' TO PLAY AGAIN", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    window.blit(restart_text, restart_rect)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boss_enemies = pygame.sprite.Group()  # New group for boss
upgrade_cubes = pygame.sprite.Group()
xp_triangles = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()  # Sprite group for enemy bullets
shoot_boosts = pygame.sprite.Group()  # New group for shoot boost
point_boosts = pygame.sprite.Group()  # New group for point boost

# Initialize player
player = None

# Play background music
def play_background_music():
    backgroundMusic.play(-1)  # -1 loops the music indefinitely

# Start background music immediately
play_background_music()

# Game variables
spawn_counter = 0
upgrade_spawn_counter = 0
xp_triangle_spawn_counter = 0
upgrade_spawn_interval = 900  # Increase this value to make yellow upgrade cubes spawn less frequently
xp_triangle_spawn_interval = 900  # Increase this value to make XP triangles spawn less frequently

# New collectible spawn variables
shoot_boost_spawn_counter = 0
point_boost_spawn_counter = 0
shoot_boost_spawn_interval = 1200  # 20 seconds
point_boost_spawn_interval = 1500  # 25 seconds

# Level system variables
current_level = 1
enemies_killed_this_level = 0
boss_spawned = False
level_complete = False

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                    reset_game()
            elif game_state == PLAYING:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    game_state = MENU

    # Update game based on current state
    if game_state == PLAYING:
        all_sprites.update()

        # Get enemies needed for current level
        enemies_needed_per_level = get_enemies_needed_for_level(current_level)

        # Level progression logic
        if current_level <= 3:
            # Spawn regular enemies for levels 1-3
            spawn_counter += 1
            if spawn_counter == 60:  # Spawn every second (60 frames per second)
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
                spawn_counter = 0
        elif current_level == 4 and not boss_spawned:
            # Spawn boss after completing level 3
            boss = BossEnemy()
            all_sprites.add(boss)
            boss_enemies.add(boss)
            boss_spawned = True

        # Spawn upgrade cubes and XP triangles for all levels
        upgrade_spawn_counter += 1
        if upgrade_spawn_counter == upgrade_spawn_interval:  # Adjust the interval
            upgrade_cube = UpgradeCube()
            all_sprites.add(upgrade_cube)
            upgrade_cubes.add(upgrade_cube)
            upgrade_spawn_counter = 0

        xp_triangle_spawn_counter += 1
        if xp_triangle_spawn_counter == xp_triangle_spawn_interval:  # Adjust the interval
            xp_triangle = XPTriangle()
            all_sprites.add(xp_triangle)
            xp_triangles.add(xp_triangle)
            xp_triangle_spawn_counter = 0

        # Spawn new collectibles
        shoot_boost_spawn_counter += 1
        if shoot_boost_spawn_counter == shoot_boost_spawn_interval:
            shoot_boost = ShootBoost()
            all_sprites.add(shoot_boost)
            shoot_boosts.add(shoot_boost)
            shoot_boost_spawn_counter = 0

        point_boost_spawn_counter += 1
        if point_boost_spawn_counter == point_boost_spawn_interval:
            point_boost = PointBoost()
            all_sprites.add(point_boost)
            point_boosts.add(point_boost)
            point_boost_spawn_counter = 0

        # Collision detection with upgrade cubes
        upgrade_hits = pygame.sprite.spritecollide(player, upgrade_cubes, True)
        if upgrade_hits:
            player.upgrade()
            play_sound(upgradeItemStart)  # Play upgrade item start sound

        # Collision detection with XP triangles
        xp_triangle_hits = pygame.sprite.spritecollide(player, xp_triangles, True)
        for xp_triangle in xp_triangle_hits:
            if player.health < 6:
                player.health += 1
                if player.health > 6:
                    player.health = 6
                play_sound(pickUpXpItem)  # Play pick up XP item sound

        # Collision detection with shoot boost
        shoot_boost_hits = pygame.sprite.spritecollide(player, shoot_boosts, True)
        if shoot_boost_hits:
            player.activate_shoot_boost()
            play_sound(upgradeItemStart)  # Play upgrade sound for shoot boost

        # Collision detection with point boost
        point_boost_hits = pygame.sprite.spritecollide(player, point_boosts, True)
        if point_boost_hits:
            player.score += 10
            play_sound(pickUpXpItem)  # Play pick up sound for point boost

        # Collision detection with enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            player.score += 1
            enemies_killed_this_level += 1
            play_sound(defetedEnemy)  # Play defeated enemy sound
            
            # Check if level is complete
            if enemies_killed_this_level >= enemies_needed_per_level and current_level <= 3:
                current_level += 1
                enemies_killed_this_level = 0
                if current_level > 3:
                    # Clear remaining enemies before boss
                    enemies.empty()

        # Collision detection with boss
        boss_hits = pygame.sprite.groupcollide(boss_enemies, bullets, False, True)
        for boss in boss_hits:
            if boss.hit():  # Boss takes damage
                player.score += 10  # Bonus points for defeating boss
                boss.kill()
                play_sound(defetedEnemy)
                level_complete = True
                game_state = GAME_OVER

        # Collision detection with player and enemies (NEW: causes damage)
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.health -= 1
                enemy.kill()
                play_sound(XpMinus)  # Play damage sound
                if player.health <= 0:
                    game_state = GAME_OVER
                    play_sound(gameOver)  # Play game over sound

        # Collision detection with player and boss
        for boss in boss_enemies:
            if pygame.sprite.collide_rect(player, boss):
                player.health -= 2  # Boss does more damage
                play_sound(XpMinus)  # Play damage sound
                if player.health <= 0:
                    game_state = GAME_OVER
                    play_sound(gameOver)  # Play game over sound

        # Collision detection with enemy bullets
        bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if bullet_hits:
            player.health -= 1
            play_sound(XpMinus)  # Play XP minus sound
            if player.health <= 0:
                game_state = GAME_OVER
                play_sound(gameOver)  # Play game over sound

    # Draw based on current state
    if game_state == MENU:
        draw_start_screen()
    elif game_state == PLAYING:
        window.fill((0, 0, 0))
        window.blit(bg_image, (0, 0))  # Draw background image

        all_sprites.draw(window)  # Draw all sprites

        # Display score
        score_text = text_font.render(f"Score: {player.score}", True, WHITE)
        window.blit(score_text, (WIDTH - 150, 10))

        # Display current level
        if current_level <= 3:
            level_text = text_font.render(f"Level: {current_level}", True, WHITE)
            window.blit(level_text, (WIDTH - 150, 50))
            enemies_needed = get_enemies_needed_for_level(current_level)
            progress_text = text_font.render(f"Enemies: {enemies_killed_this_level}/{enemies_needed}", True, WHITE)
            window.blit(progress_text, (WIDTH - 200, 90))
        elif current_level == 4:
            boss_text = text_font.render("BOSS FIGHT!", True, RED)
            window.blit(boss_text, (WIDTH - 150, 50))
            # Display boss health if boss exists
            for boss in boss_enemies:
                boss_health_text = text_font.render(f"Boss HP: {boss.health}/{boss.max_health}", True, RED)
                window.blit(boss_health_text, (WIDTH - 180, 90))

        # Display health bar
        pygame.draw.rect(window, GRAY, (10, 10, 200, 30))
        health_width = player.health * 33.33
        if player.health >= 4:
            color = GREEN
        elif player.health >= 2:
            color = ORANGE
        else:
            color = RED
        pygame.draw.rect(window, color, (10, 10, health_width, 30))

        # Display hx indicator
        hx_text = text_font.render(f"HX: {player.health}", True, WHITE)
        window.blit(hx_text, (220, 10))

        # Display upgrade timer
        if player.upgraded:
            upgrade_timer_text = text_font.render(f"Upgrade: {15 - player.upgrade_timer // 60}", True, WHITE)
            window.blit(upgrade_timer_text, (10, 50))

        # Display shoot boost timer
        if player.shoot_boost_active:
            shoot_boost_timer_text = text_font.render(f"Auto Shoot: {10 - player.shoot_boost_timer // 60}", True, BLUE)
            window.blit(shoot_boost_timer_text, (10, 90))

    elif game_state == GAME_OVER:
        draw_game_over_screen(level_complete)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()