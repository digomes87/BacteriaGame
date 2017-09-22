import pygame
import math
from constants import *
from pygame.locals import *

class Antibody:
    """this class manages and draws (with lines, rotation...) individual antybody objects"""

    def __init__(self, x, y, dx, dy, r, dr):
        self.dx = dx
        self.dy = dy
        self.dr = dr
        self.x = x
        self.y = y
        self.r = r
        self.AABB = [-ANTIBODY_LINE_LENGTH/2.0, -ANTIBODY_LINE_LENGTH/2.0,
                     ANTIBODY_LINE_LENGTH, ANTIBODY_LINE_LENGTH]

    def render(self, screen, x_scroll):
        self.draw_angular_line(self.r, screen, x_scroll)
        self.draw_angular_line(self.r + math.pi*2/3, screen, x_scroll)
        self.draw_angular_line(self.r + math.pi*4/3, screen, x_scroll)

    def draw_angular_line(self, angle, screen, x_scroll):
        """this function draws a line on the screen, with polar coordinates"""
        delta_x = math.cos(angle)
        delta_y = math.sin(angle)
        pygame.draw.line(screen,
                         ANTIBODY_COLOR,
                         (self.x - x_scroll, self.y),
                         (self.x - x_scroll+ANTIBODY_LINE_LENGTH*delta_x, self.y+ANTIBODY_LINE_LENGTH*delta_y),
                         2)

    def gravity(self, time):
            self.dy += GRAVITY * time

    def move(self, time):
        """move acording to linear and angular velocity"""
        self.x += self.dx * time
        self.y += self.dy * time
        self.r += self.dr * time

    def absolute_aabb(self):
        """return the aabb relative to the universe origin"""
        return [self.AABB[X]+self.x,
                self.AABB[Y]+self.y,
                self.AABB[W],
                self.AABB[H]]