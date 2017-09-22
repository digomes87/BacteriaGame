import pygame
import math
import random as rand
from constants import *
from pygame.locals import *
from Antibody import *
from Mob import *
from InfoText import *

class MobManager:
    """this class will manager all the differant mobs in the game
    and their interacton (collision detection...)"""

    def __init__(self):
        self.player_bullets = list()
        self.energy_balls = list()
        self.enemy_bacteria = list()
        self.antibodies = list()
        self.enemy_bullets = list()

        self.texts = InfoText(pygame.font.Font("font.ttf", 12))

    def move(self, time, game):
        for i in range(len(self.enemy_bacteria)):
            self.enemy_bacteria[i].gravity(time)
            self.enemy_bacteria[i].move(time, game)
        for i in range(len(self.player_bullets)):
            self.player_bullets[i].gravity(time)
            self.player_bullets[i].move(time)
        for i in range(len(self.energy_balls)):
            self.energy_balls[i].gravity(time)
            self.energy_balls[i].move(time)
        for i in range(len(self.antibodies)):
            self.antibodies[i].gravity(time)
            self.antibodies[i].move(time)
        for i in range(len(self.enemy_bullets)):
            self.enemy_bullets[i].gravity(time)
            self.enemy_bullets[i].move(time)

    def interact(self, game):
        """all the collision detection and consequential actions"""
        # antibody-bacterial collision
        antibody_deletion_list = list()
        updated_antibodies_list = list()
        for antibody in range(len(self.antibodies)):
            for enemy in range(len(self.enemy_bacteria)):
                if not self.enemy_bacteria[enemy].is_neutralized:
                    if inter_AABB_collision(self.antibodies[antibody].absolute_aabb(), self.enemy_bacteria[enemy].absolute_aabb()):
                        self.enemy_bacteria[enemy].antibody_added(game)
                        antibody_deletion_list.append(antibody)
        for i in range(len(self.antibodies)):
            if i not in antibody_deletion_list:
                updated_antibodies_list.append(self.antibodies[i])
        self.antibodies = updated_antibodies_list

        # bullet-bacterial collision
        bullet_deletion_list = list()
        updated_bullet_list = list()
        for bullet in range(len(self.player_bullets)):
            for enemy in range(len(self.enemy_bacteria)):
                if inter_AABB_collision(self.player_bullets[bullet].absolute_aabb(), self.enemy_bacteria[enemy].absolute_aabb()):
                    self.enemy_bacteria[enemy].recieved_bullet()
                    bullet_deletion_list.append(bullet)
        for i in range(len(self.player_bullets)):
            if i not in bullet_deletion_list:
                updated_bullet_list.append(self.player_bullets[i])
        self.player_bullets = updated_bullet_list
        self.check_for_dead_bacteria()

        # enemy-bullet - player
        enemy_bullet_deletion_list = list()
        updated_enemy_bullet_list = list()
        for bullet in range(len(self.enemy_bullets)):
            if inter_AABB_collision(self.enemy_bullets[bullet].absolute_aabb(), game.player.absolute_aabb()):
                game.player.get_enemy_bullet(game)
                enemy_bullet_deletion_list.append(bullet)
        for i in range(len(self.enemy_bullets)):
            if i not in enemy_bullet_deletion_list:
                updated_enemy_bullet_list.append(self.enemy_bullets[i])
        self.enemy_bullets = updated_enemy_bullet_list
        self.check_for_dead_bacteria()

        # energy - player
        energy_ball_deletion_list = list()
        updated_energy_ball_list = list()
        for ball in range(len(self.energy_balls)):
            if inter_AABB_collision(self.energy_balls[ball].absolute_aabb(), game.player.absolute_aabb()):
                game.player.get_energy_ball(game)
                energy_ball_deletion_list.append(ball)
        for i in range(len(self.energy_balls)):
            if i not in energy_ball_deletion_list:
                updated_energy_ball_list.append(self.energy_balls[i])
        self.energy_balls = updated_energy_ball_list
        self.check_for_dead_bacteria()

        # bacterial player proximity
        for bacteria in self.enemy_bacteria:
            if abs(bacteria.absolute_aabb()[X] + bacteria.absolute_aabb()[W]/2.0 - game.player.absolute_aabb()[X] - game.player.absolute_aabb()[W]/2.0) < BACTERIA_PISSED_OFF_PROXIMITY_THRESHOLD:
                if not bacteria.is_neutralized:
                    bacteria.state = bacteria.type + PISSED_OFF_STATE_SHIFT
                else:
                    bacteria.state = bacteria.type + NORMAL_STATE_SHIFT
            else:
                bacteria.state = bacteria.type + NORMAL_STATE_SHIFT
        for bacteria in self.enemy_bacteria:
            if bacteria.state == BACTERIA_1_STATE_PISSED_OFF:
                if not rand.randrange(ENEMY_BULLET_PERIOD):
                    self.shoot_enemy_bullet(AABB_center(bacteria.absolute_aabb()), BACTERIA_1_BULLET_MAX_NUMBER)
            elif bacteria.state == BACTERIA_2_STATE_PISSED_OFF:
                if not rand.randrange(ENEMY_BULLET_PERIOD):
                    self.shoot_enemy_bullet(AABB_center(bacteria.absolute_aabb()), BACTERIA_2_BULLET_MAX_NUMBER)

        # bacterial player proximity 2
        for bacteria in self.enemy_bacteria:
            if abs(bacteria.absolute_aabb()[X] + bacteria.absolute_aabb()[W]/2.0 - game.player.absolute_aabb()[X] - game.player.absolute_aabb()[W]/2.0) < BACTERIA_MOVEMENT_PROXIMITY_THRESHOLD:
                if not bacteria.is_neutralized:
                    if game.player.x > bacteria.x:
                        bacteria.dx = BACTERIA_SPEED
                    else:
                        bacteria.dx = -BACTERIA_SPEED
                else:
                    bacteria.dx = 0
            else:
                bacteria.dx = 0

        #player - bacteria not neutraliezed
        for bacteria in self.enemy_bacteria:
            if not bacteria.is_neutralized:
                if inter_AABB_collision(bacteria.absolute_aabb(), game.player.absolute_aabb()):
                    game.player.bacteria_contact(game)


    def render(self, screen, x_scroll):
        for i in range(len(self.enemy_bacteria)):
            self.enemy_bacteria[i].render(screen, x_scroll)
        for i in range(len(self.player_bullets)):
            self.player_bullets[i].render(screen, x_scroll)
        for i in range(len(self.energy_balls)):
            self.energy_balls[i].render(screen, x_scroll)
        for i in range(len(self.antibodies)):
            self.antibodies[i].render(screen, x_scroll)
        for i in range(len(self.enemy_bullets)):
            self.enemy_bullets[i].render(screen, x_scroll)

    def show_aabbs(self, screen, x_scroll = 0):
        """for debug purposes"""
        for i in range(len(self.enemy_bacteria)):
            tmp_aabb = self.enemy_bacteria[i].absolute_aabb()
            screen.fill((210, 26, 54), (tmp_aabb[X] - x_scroll, tmp_aabb[Y], tmp_aabb[W], tmp_aabb[H]))
        for i in range(len(self.player_bullets)):
            self.player_bullets[i].move()
        for i in range(len(self.energy_balls)):
            self.energy_balls[i].move()
        for i in range(len(self.antibodies)):
            tmp_aabb = self.antibodies[i].absolute_aabb()
            screen.fill((210, 26, 54), (tmp_aabb[X] - x_scroll, tmp_aabb[Y], tmp_aabb[W], tmp_aabb[H]))

    def cast_antibodies(self, origin, game):
        game.play_sound(SOUND_ANTIBODIES)
        for i in range(rand.randrange(10, 22)):
            r = rand.randrange(int((1000*math.pi)/6.0+0.5), int((1000*math.pi)/3.0+0.5))/1000.0  # random angle
            self.antibodies.append(Antibody(origin[X],
                                   origin[Y],
                                   ANTIBODY_CAST_SPEED*math.cos(r)*rand.randrange(800, 1200)/1000.0,
                                   -ANTIBODY_CAST_SPEED*math.sin(r)*rand.randrange(800, 1200)/1000.0,
                                   rand.randrange(int(-math.pi*1000), int(math.pi*1000))/1000.0,
                                   rand.randrange(1, 15)/1000.0))

    def shoot_bullet(self, origin):
        self.player_bullets.append(Mob(BULLET, origin[X], origin[Y], BULLET_SPEED, -0.2*BULLET_SPEED))

    def shoot_enemy_bullet(self, origin, max_quantity):
        for i in range(abs(rand.randrange(max_quantity)+1)):
            angle = rand.randrange(int(math.pi*1000/6.0 + 0.5), int(1000*math.pi*5/6.0 + 0.5))/1000.0
            self.enemy_bullets.append(Mob(ENEMY_BULLET, origin[X], origin[Y],
                                          math.cos(angle) * ENEMY_BULLET_SPEED * rand.randrange(800, 1200)/1000.0,
                                          -math.sin(angle) * ENEMY_BULLET_SPEED * rand.randrange(800, 1200)/1000.0))

    def check_for_dead_bacteria(self):
        bacteria_deletion_list = list()
        updated_bacteria_list = list()
        for i in range(len(self.enemy_bacteria)):
            if self.enemy_bacteria[i].health == 0:
                for n in range(rand.randrange(3)+1):
                    self.energy_balls.append(Mob(ENERGY,
                                             self.enemy_bacteria[i].x + rand.randrange(self.enemy_bacteria[i].AABB[W]),
                                             self.enemy_bacteria[i].y, 0, -0.03))
                bacteria_deletion_list.append(i)
        for i in range(len(self.enemy_bacteria)):
            if i not in bacteria_deletion_list:
                updated_bacteria_list.append(self.enemy_bacteria[i])
        self.enemy_bacteria = updated_bacteria_list

    def antibody_cleanup(self, x_scroll):
        """delete lost antibodies (off screen) for memory saving"""
        antibody_deletion_list = list()
        updated_antibodies_list = list()
        for i in range(len(self.antibodies)):
            if not inter_AABB_collision(self.antibodies[i].absolute_aabb(),
                                        (x_scroll, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                    antibody_deletion_list.append(i)
        for i in range(len(self.antibodies)):
            if i not in antibody_deletion_list:
                updated_antibodies_list.append(self.antibodies[i])
        self.antibodies = updated_antibodies_list

    def bullet_cleanup(self, x_scroll):
        """delete lost bullets (off screen) for memory saving"""
        bullet_deletion_list = list()
        updated_bullets_list = list()
        for i in range(len(self.player_bullets)):
            if not inter_AABB_collision(self.player_bullets[i].absolute_aabb(),
                                        (x_scroll, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                    bullet_deletion_list.append(i)
        for i in range(len(self.player_bullets)):
            if i not in bullet_deletion_list:
                updated_bullets_list.append(self.player_bullets[i])
        self.player_bullets = updated_bullets_list

    def enemy_bullet_cleanup(self, x_scroll):
        """delete lost bullets (off screen) for memory saving"""
        bullet_deletion_list = list()
        updated_bullets_list = list()
        for i in range(len(self.enemy_bullets)):
            if not inter_AABB_collision(self.enemy_bullets[i].absolute_aabb(),
                                        (x_scroll, 0, SCREEN_WIDTH, SCREEN_HEIGHT)):
                    bullet_deletion_list.append(i)
        for i in range(len(self.enemy_bullets)):
            if i not in bullet_deletion_list:
                updated_bullets_list.append(self.enemy_bullets[i])
        self.enemy_bullets = updated_bullets_list