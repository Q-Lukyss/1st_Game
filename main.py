# This is a sample Python script.
import random

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


class Enemies(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "snail":
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        elif type == "fly":
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score : {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5

            if obstacle_rectangle.bottom == 300:
                screen.blit(snail_surface, obstacle_rectangle)
            else:
                screen.blit(fly_surface, obstacle_rectangle)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        enemies_group.empty()
        return False
    else: return True

def player_animation():
    global player_surface, player_index
    # Animation de marche si le joeur est au sol
    # Animation de saut si le joueur saute
    if player_rectangle.bottom < 300:
        # Jump
        player_surface = player_jump
    else:
        # Walk
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


# Initialiser pygame
# Definir les proprietes de la fenetre width*height
# Definir le Titre
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Lukyss' Little World")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/down-from-the-sky.wav")
# bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play()
bg_music.play(loops=-1)
bg_music.set_volume(0.5)

# Code Exemple pour un surface unie
# test_surface = pygame.Surface((100, 200))
# test_surface.fill("Red")

# Code Exemple une surface image
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

# Code Exemple pour une surface Texte
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# text_surface = test_font.render("Lukyss' Little World", False, (64,64,64))
# text_rectangle = text_surface.get_rect(center = (400, 50))

# Enemis
# Snails
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
# Flies
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

# Groupes
player = pygame.sprite.GroupSingle()
player.add(Player())

enemies_group = pygame.sprite.Group()

# Player
# Plqcer une Surface dans un rectangle pour mieux positionner l'element
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
# Prend une Surface et dessine un Rectangle autour
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Ecran d'Intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = test_font.render("Lukyss' Little World", False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Cliquez sur [Espace] pour Jouer", False, (111, 196, 169))
game_message_rectangle = game_message.get_rect(center=(400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# Permettre a la Fenetre de ne pas disparaitre
# Boucle de Jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            # Timer pour les obstacles
            if event.type == obstacle_timer:
                enemies_group.add(Enemies(choice(["fly", "snail", "snail", "snail"])))
                # if randint(0, 2):
                #     obstacle_rectangle_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rectangle_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 210)))

            # Timer pour les snails
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            # Timer pour les flies
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        # Dessiner tous nos elements
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # pygame.draw.rect(screen, "#c0e8ec", text_rectangle)
        #
        # screen.blit(text_surface, text_rectangle)
        score = display_score()

        # On Decremente la position pour faire se deplacer le snail vers la gauche
        # snail_rectangle.left -= 4
        # # S'il sort de l'ecran, on le refait spawn a drotie
        # if snail_rectangle.right <= 0: snail_rectangle.left = 800
        # screen.blit(snail_surface, snail_rectangle)

        # Player
        # player_gravity += 1
        # player_rectangle.bottom += player_gravity
        # if player_rectangle.bottom >= 300:
        #     player_rectangle.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rectangle)
        player.draw(screen)
        player.update()

        enemies_group.draw(screen)
        enemies_group.update()

        # Ennemis mouvement
        # obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # Collision
        # game_active = collision(player_rectangle, obstacle_rectangle_list)
        game_active = collision_sprite()


    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)

        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f'Votre Score : {score}', False, (111, 196, 169))
        score_message_rectangle = score_message.get_rect(center=(400, 340))
        screen.blit(game_name, game_name_rectangle)
        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    # Tout mettre a jour
    pygame.display.update()
    # Definir la vitesse d'image a maximum 60fps
    clock.tick(60)
