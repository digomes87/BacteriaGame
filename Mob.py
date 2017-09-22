import pygame
from constants import *

class Mob:
    """this class manages any kind of mob"""

    def __init__(self, type, x, y, dx, dy):
        if type == BULLET:
            self.img = pygame.image.load("chem-bullet.png").convert_alpha()
            self.ground_receptive = False
        elif type == ENERGY:
            self.img = pygame.image.load("energy.png").convert_alpha()
            self.ground_receptive = True
        elif type == ENEMY_BULLET:
            self.img = pygame.image.load("enemy-bullet.png").convert_alpha()
            self.ground_receptive = False

        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.AABB = AABB_crop([0, 0, self.img.get_width(), self.img.get_height()], 8)

    def render(self, screen, x_scroll=0):
        screen.blit(self.img, (self.x - x_scroll, self.y))

    def gravity(self, time):
        if self.ground_receptive:
            if self.y + self.AABB[H] < FLOOR_Y:
                self.dy += GRAVITY * time
            else:
                self.y = FLOOR_Y - self.AABB[H]
                self.dy = 0
        else:
            self.dy += GRAVITY * time

    def move(self, time):
        """move acording to linear and angular velocity"""
        self.x += self.dx * time
        self.y += self.dy * time

    def absolute_aabb(self):
        """return the aabb relative to the universe origin"""
        return [self.AABB[X]+self.x,
                self.AABB[Y]+self.y,
                self.AABB[W],
                self.AABB[H]]