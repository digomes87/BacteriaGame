import pygame
import random as rand
from constants import *
from pygame.locals import *

class Player:
    """this class manages the player interactions"""

    def __init__(self, texts):
        self.img = pygame.image.load("player.png").convert_alpha()
        self.x = PLAYER_INITIAL_X
        self.y = FLOOR_Y - self.img.get_height() - 50
        self.dx = 0
        self.dy = 0
        self.AABB = AABB_crop([0, 0, self.img.get_width(), self.img.get_height()], 8)
        self.rel_shoot_point = (self.img.get_width()*2/3, self.img.get_height()/2)
        self.texts = texts

        self.health = 100
        self.energy = 100

        self.font_text = pygame.font.Font("font.ttf", 16)

    def render(self, screen, x_scroll):
        screen.blit(self.img, (self.x - x_scroll, self.y))
        self.render_ui(screen)

    def render_ui(self, screen):
        if self.energy > 0:
            energy_bar = pygame.Surface(((ENERGY_BAR_WIDTH*self.energy)/100.0, ENERGY_BAR_HEIGHT), SRCALPHA)
            energy_bar.fill(ENERGY_ORANGE)
            screen.blit(energy_bar, (0, 0))
        if self.health > 0:
            membrane_bar = pygame.Surface(((MEMBRANE_BAR_WIDTH*self.health)/100.0, MEMBRANE_BAR_HEIGHT), SRCALPHA)
            membrane_bar.fill(MEMBRANE_GREEN)
            screen.blit(membrane_bar, (0, 20))

        screen.blit(self.font_text.render("Energy ("+str(int(self.energy*10)/10.0)+"%)", 1, WHITE), (5, 0))
        screen.blit(self.font_text.render("Membrane ("+str(int(self.health*10)/10.0)+"%)", 1, WHITE), (5, 22))

    def gravity(self, time):
        if self.y + self.AABB[H] < FLOOR_Y:
             self.dy += GRAVITY * time
        else:
             self.y = FLOOR_Y - self.AABB[H]
             self.dy = 0

    def move(self, time):
        self.x += self.dx * time
        self.y += self.dy * time
        self.energy -= PLAYER_ENERGY_DECAY_RATE
        if self.health < 100:
            self.health += PLAYER_MEMBRANE_HEAL_RATE
            self.energy -= 3*PLAYER_ENERGY_DECAY_RATE
        if self.energy < 0:
            self.health += self.energy
            self.energy = 0

    def absolute_aabb(self):
        """return the aabb relative to the universe origin"""
        return [self.AABB[X]+self.x,
                self.AABB[Y]+self.y,
                self.AABB[W],
                self.AABB[H]]

    def absolute_shoot_point(self):
        return (self.rel_shoot_point[X] + self.x, self.rel_shoot_point[Y] + self.y)

    def get_enemy_bullet(self, game):
        damage = rand.randrange(ENEMY_BULLET_DAMAGE - 1, ENEMY_BULLET_DAMAGE + 2)
        self.health -= damage
        game.play_sound(BULLET)
        if self.health < 0:
            self.health = 0
            game.game_over()
        pos = AABB_center(self.absolute_aabb())
        self.texts.add_text('-'+str(damage), 14, (255, 42, 42), [rand.randrange(int(pos[X]-20), int(pos[X]+20)), pos[Y]], [0, -0.08], 1600)

    def get_energy_ball(self, game):
        increase = rand.randrange(ENERGY_BALL_INCREASE - 1, ENERGY_BALL_INCREASE + 2)
        game.play_sound(ENERGY)
        self.energy += increase
        pos = AABB_center(self.absolute_aabb())
        self.texts.add_text('+'+str(increase), 14, (42, 255, 42), [rand.randrange(int(pos[X]-20), int(pos[X]+20)), pos[Y]], [0, -0.08], 1600)

    def bacteria_contact(self, game):
        if rand.randrange(2):
            self.get_enemy_bullet(game)