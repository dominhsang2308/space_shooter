import pygame
import sys
import random
from ntpath import join
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 500
    #cooldown laser
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 500 # milliseconds

    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    def movement(self,dt):
        self.direction.x = int(pygame.key.get_pressed()[pygame.K_RIGHT]) - int(pygame.key.get_pressed()[pygame.K_LEFT])
        self.direction.y = int(pygame.key.get_pressed()[pygame.K_DOWN]) - int(pygame.key.get_pressed()[pygame.K_UP])
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        else:
            self.direction = self.direction
        self.rect.center += self.direction * self.speed * dt
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), lasor_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_time()
    def update(self,dt):
        self.movement(dt)

class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,groups,surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self,dt):
        self.rect.y -= 500 * dt
        if self.rect.bottom < 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, groups, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 5000 #miliseconds
        self.direction = pygame.math.Vector2(random.uniform(-0.5,0.5),1).normalize()
        self.speed = random.randint(400,500)
    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()

def collision_sprite():
    #event collision sprites
    player_hit = pygame.sprite.spritecollide(player, meteor_sprites, False)
    if player_hit:
        print("Player hit!")

    for laser in laser_sprites:
        meteors_hit = pygame.sprite.spritecollide(laser,meteor_sprites, True)
        if meteors_hit:
            laser.kill()

#import 
metor_surf = pygame.image.load(join("images", "meteor.png")).convert_alpha()
lasor_surf = pygame.image.load(join("images", "laser.png")).convert_alpha()
#sprite group
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join("images", "star.png")).convert_alpha()
for i in range(20):
    star = Star(all_sprites,star_surf)

player = Player(all_sprites)
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(join("images", "Pixeltype.ttf"), 50)
font_surface = font.render("Scores : 0", False, (255,255,255))
#surface
surf = pygame.Surface((200,150))
star_positions = []

for i in range(20):
    x = random.randint(0, WINDOW_WIDTH)
    y = random.randint(0, WINDOW_HEIGHT)
    star_positions.append((x,y))
    

#custom event timer
meteor = pygame.event.custom_type()
pygame.time.set_timer(meteor, 500)

while running:
    dt = clock.tick()/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        x,y = random.randint(0, WINDOW_WIDTH), random.randint(-200, 100)
        if event.type == meteor:
            Meteor(metor_surf, (all_sprites, meteor_sprites),((x,y)))
    screen.fill((143, 77, 126))
    collision_sprite()
    #update 
    all_sprites.update(dt)
    #draw        
    all_sprites.draw(screen)
    screen.blit(font_surface, (10,10))
    pygame.display.update()
pygame.quit()