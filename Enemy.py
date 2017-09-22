import pygame
import random as rand
from constants import *
from pygame.locals import *
from InfoText import *

class Enemy:
    """this class will manage all the individual bacterial mobs"""

    def __init__(self, type, x, dx):
        self.img = pygame.image.load("enemy-"+str(type)+".png").convert_alpha()
        self.neutralized_img = pygame.image.load("enemy-"+str(type)+"-neutralized.png").convert_alpha()
        self.x = x
        self.y = FLOOR_Y - self.img.get_height()
        self.dx = dx
        self.dy = 0
        self.type = type
        self.AABB = AABB_crop([0, 0, self.img.get_width(), self.img.get_height()], 20)

        self.is_neutralized = False
        self.n_antibodies = 0
        self.state = type+NORMAL_STATE_SHIFT
        self.health = 100
        self.time_since_full_health_and_neutralized = 0

        self.texts = InfoText(pygame.font.Font("font.ttf", 22))

    def render(self, screen, x_scroll):
        if not self.is_neutralized:
            screen.blit(self.img, (self.x - x_scroll, self.y))
            if self.health != 100:
                rect = (self.x - x_scroll, self.y - HEALTHBAR_HEIGHT, self.img.get_width(), HEALTHBAR_HEIGHT)
                healthbar = pygame.Surface((rect[W], rect[H]), SRCALPHA)
                healthbar.fill(HEALTHBAR_BG_GREEN)
                healthbar.fill(HEALTHBAR_GREEN, (0, 0, rect[W]*(self.health/100.0), HEALTHBAR_HEIGHT))
                screen.blit(healthbar, (rect[X], rect[Y]))
        else:
            screen.blit(self.neutralized_img, (self.x - x_scroll, self.y))
            if self.health != 100:
                rect = (self.x - x_scroll, self.y - HEALTHBAR_HEIGHT, self.neutralized_img.get_width(), HEALTHBAR_HEIGHT)
                healthbar = pygame.Surface((rect[W], rect[H]), SRCALPHA)
                healthbar.fill(HEALTHBAR_BG_GREEN)
                healthbar.fill(HEALTHBAR_GREEN, (0, 0, rect[W]*(self.health/100.0), HEALTHBAR_HEIGHT))
                screen.blit(healthbar, (rect[X], rect[Y]))
        self.texts.render(screen, x_scroll)

    def gravity(self, time):
        if self.y + self.AABB[H] < FLOOR_Y:
             self.dy += GRAVITY * time
        else:
             self.y = FLOOR_Y - self.AABB[H]
             self.dy = 0

    def move(self, time, game):
        self.x += self.dx * time
        self.y += self.dy * time
        # repairs
        if self.health < 100:
            self.health += time * BACTERIA_REPAIR_SPEED
        else:
            if self.is_neutralized:
                self.time_since_full_health_and_neutralized += time
        if self.time_since_full_health_and_neutralized > BACTERIA_DENEUTRALIZATION_THRESHOLD:
            self.time_since_full_health_and_neutralized = 0
            self.is_neutralized = False
            self.n_antibodies = 0
            self.texts.add_text("Deneuralized", 14, WHITE, self.absolute_aabb(), [0, -0.08], 1600)
            game.play_sound(SOUND_DENEUTRALIZE)

        self.texts.move(time)

    def antibody_added(self, game):
        self.n_antibodies += 1
        if self.type == BACTERIA_1:
            if self.n_antibodies > BACTERIA_1_ANTIBODY_NEUTRALISATION_THRESHOLD:
                self.is_neutralized = True
                self.texts.add_text("Neuralized", 14, (255, 42, 42), self.absolute_aabb(), [0, -0.08], 1600)
                game.play_sound(SOUND_NEUTRALIZE)
        elif self.type == BACTERIA_2:
            if self.n_antibodies > BACTERIA_2_ANTIBODY_NEUTRALISATION_THRESHOLD:
                self.is_neutralized = True
                self.texts.add_text("Neuralized", 14, (255, 42, 42), self.absolute_aabb(), [0, -0.08], 1600)
                game.play_sound(SOUND_NEUTRALIZE)

    def absolute_aabb(self):
        """return the aabb relative to the universe origin"""
        return [self.AABB[X]+self.x,
                self.AABB[Y]+self.y,
                self.AABB[W],
                self.AABB[H]]

    def recieved_bullet(self):
        damage = BULLET_DAMAGE + rand.randrange(4)
        self.health -= damage
        if self.health < 0:
            self.health = 0