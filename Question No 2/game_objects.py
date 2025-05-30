# This file has all the game characters and items like player, enemies, bullets etc.
# Basically everything that moves or appears in the game is defined here

import pygame
import random

# Player class - this is our main character
class Player(pygame.sprite.Sprite):
    def __init__(self, ship_without_upgrade_image, ship_upgrade_image):
        super().__init__()
        self.original_image = ship_without_upgrade_image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.left = 10  # start from left side
        self.rect.centery = 350  # center it vertically
        self.speed = 5
        self.double_shooter = False
        self.upgraded = False
        self.upgrade_timer = 0
        self.score = 0
        self.health = 6
        
        # shoot boost stuff
        self.shoot_boost_active = False
        self.shoot_boost_timer = 0
        self.auto_shoot_counter = 0
        
        # store the upgrade image
        self.ship_upgrade_image = ship_upgrade_image

    def update(self):
        keys = pygame.key.get_pressed()
        # movement controls
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # make sure player stays on screen
        self.rect.clamp_ip(pygame.Rect(0, 0, 1000, 700))

        # upgrade timer stuff
        if self.upgraded:
            self.upgrade_timer += 1
            if self.upgrade_timer >= 900:  # 15 seconds
                self.downgrade()
        
        # shoot boost timer
        if self.shoot_boost_active:
            self.shoot_boost_timer += 1
            self.auto_shoot_counter += 1
            
            # auto shoot every 10 frames
            if self.auto_shoot_counter >= 10:
                self.shoot()
                self.auto_shoot_counter = 0
            
            # stop after 10 seconds
            if self.shoot_boost_timer >= 600:
                self.shoot_boost_active = False
                self.shoot_boost_timer = 0
        
        # change speed when upgraded
        if self.upgraded:
            self.speed = 8
        else:
            self.speed = 5

    def upgrade(self):
        self.upgraded = True
        self.original_image = self.ship_upgrade_image
        self.image = self.original_image.copy()
        self.double_shooter = True
        self.upgrade_timer = 0

    def downgrade(self):
        self.upgraded = False
        self.original_image = pygame.image.load('Images/tank_without_upgrade.png')
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.image = self.original_image.copy()
        self.double_shooter = False

    def activate_shoot_boost(self):
        self.shoot_boost_active = True
        self.shoot_boost_timer = 0
        self.auto_shoot_counter = 0

    def shoot(self):
        from main import all_sprites, bullets, bulletShoot
        
        if self.double_shooter:  # double bullets when upgraded
            bullet1 = Bullet(self.rect.right, self.rect.top)
            bullet2 = Bullet(self.rect.right, self.rect.bottom)
            all_sprites.add(bullet1, bullet2)
            bullets.add(bullet1, bullet2)
        else:
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
        bulletShoot.play()

# Regular bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))  # white color
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > 1000:  # remove when off screen
            self.kill()

# Enemy bullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))  # red color
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.centery = y
        self.speed = -5  # goes left

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

# Basic enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = 1000  # start from right
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(1, 2)
        self.shoot_probability = 0.01

    def update(self):
        from main import all_sprites, enemy_bullets, XpMinus, enemyBulletShoot
        
        self.rect.x -= self.speed
        if self.rect.right < 0:  # respawn when off screen
            self.rect.x = 1000
            self.rect.y = random.randint(0, 600)
            self.speed = random.randint(1, 2)
            XpMinus.play()

        # sometimes shoot at player
        if random.random() <= self.shoot_probability:
            self.shoot()

    def shoot(self):
        from main import all_sprites, enemy_bullets, enemyBulletShoot
        
        bullet = EnemyBullet(self.rect.left, self.rect.centery)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        enemyBulletShoot.play()

# Boss enemy - bigger and stronger
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()
        # make boss bigger
        self.image = pygame.transform.scale(enemy_image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.centery = 350  # center vertically
        self.speed = 1  # slower
        self.health = 10  # more health
        self.max_health = 10
        self.shoot_probability = 0.05  # shoots more

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 1000
            self.rect.centery = 350

        # shoot more often
        if random.random() <= self.shoot_probability:
            self.shoot()

    def shoot(self):
        from main import all_sprites, enemy_bullets, enemyBulletShoot
        
        # boss shoots 3 bullets at once
        bullet1 = EnemyBullet(self.rect.left, self.rect.top + 30)
        bullet2 = EnemyBullet(self.rect.left, self.rect.centery)
        bullet3 = EnemyBullet(self.rect.left, self.rect.bottom - 30)
        all_sprites.add(bullet1, bullet2, bullet3)
        enemy_bullets.add(bullet1, bullet2, bullet3)
        enemyBulletShoot.play()

    def hit(self):
        self.health -= 1
        return self.health <= 0  # returns true when boss dies

# Upgrade cube - makes player stronger
class UpgradeCube(pygame.sprite.Sprite):
    def __init__(self, upgrade_image):
        super().__init__()
        self.image = upgrade_image
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(4, 6)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 1000
            self.rect.y = random.randint(0, 600)
            self.speed = random.randint(4, 6)

# XP triangle - gives health back
class XPTriangle(pygame.sprite.Sprite):
    def __init__(self, xp_image):
        super().__init__()
        self.image = xp_image
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 1000
            self.rect.y = random.randint(0, 600)
            self.speed = random.randint(1, 3)

# Shoot boost - auto shooting for a while
class ShootBoost(pygame.sprite.Sprite):
    def __init__(self, shoot_boost_image):
        super().__init__()
        self.image = shoot_boost_image
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 1000
            self.rect.y = random.randint(0, 600)
            self.speed = random.randint(3, 5)

# Point boost - gives extra points
class PointBoost(pygame.sprite.Sprite):
    def __init__(self, point_boost_image):
        super().__init__()
        self.image = point_boost_image
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = random.randint(0, 600)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = 1000
            self.rect.y = random.randint(0, 600)
            self.speed = random.randint(3, 5)