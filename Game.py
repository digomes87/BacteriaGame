import pygame
import random as rand
from Mob import *
from Enemy import *
from Player import *
from Antibody import *
from InfoText import *
from constants import *
from MobManager import *
from pygame.locals import *

class Game:
    """This class is used to manage the differant game components"""

    def __init__(self, screen):
        # big bang : creation of space and time
        self.screen = screen
        self.background = pygame.image.load("background.jpg").convert()
        self.floor = pygame.image.load("ground.jpg").convert()
        self.floor_shift = 0
        self.x_scroll = 0

        self.sounds = list()
        self.sounds.append(pygame.mixer.Sound("antibodies.wav"))
        self.sounds.append(pygame.mixer.Sound("chem-bullet.wav"))
        self.sounds.append(pygame.mixer.Sound("deneutralize.wav"))
        self.sounds.append(pygame.mixer.Sound("end.wav"))
        self.sounds.append(pygame.mixer.Sound("enemy-bullet.wav"))
        self.sounds.append(pygame.mixer.Sound("energy.wav"))
        self.sounds.append(pygame.mixer.Sound("neutralize.wav"))
        self.sounds.append(pygame.mixer.Sound("start.wav"))
        self.play_sound(SOUND_START)

        self.clock = pygame.time.Clock()
        self.frame_duration_ms = 1000/30  # temp value, will be continually updated
        self.last_time_completion_indicaiton = pygame.time.get_ticks()

        self.texts = InfoText(pygame.font.Font("font.ttf", 22))
        self.texts.add_text("Good Luck ! :p", 40, WHITE, [300, 300], [0, -0.05], 1800)

        self.player = Player(self.texts) #pass text
        self.mob_manager = MobManager()
        for i in range(20):
            self.mob_manager.enemy_bacteria.append(Enemy(BACTERIA_1, rand.randrange(SCREEN_WIDTH, WORLD_SIZE-SCREEN_WIDTH), 0))
        for i in range(20):
            self.mob_manager.enemy_bacteria.append(Enemy(BACTERIA_1, rand.randrange(WORLD_SIZE//4, WORLD_SIZE-SCREEN_WIDTH), 0))
        for i in range(20):
            self.mob_manager.enemy_bacteria.append(Enemy(BACTERIA_2, rand.randrange(WORLD_SIZE//3, WORLD_SIZE-SCREEN_WIDTH), 0))
        for i in range(20):
            self.mob_manager.enemy_bacteria.append(Enemy(BACTERIA_2, rand.randrange(WORLD_SIZE//2, WORLD_SIZE-SCREEN_WIDTH), 0))
        for i in range(10):
            self.mob_manager.enemy_bacteria.append(Enemy(BACTERIA_2, rand.randrange(WORLD_SIZE - 5*SCREEN_WIDTH, WORLD_SIZE-SCREEN_WIDTH), 0))

        self.user_presses_right = False
        self.user_presses_left = False
        self.running = True
        self.game_state = 1
        self.start_time = pygame.time.get_ticks()
        self.main_loop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.mob_manager.cast_antibodies(self.player.absolute_shoot_point(), self)
                    self.player.energy -= ANTIBODY_ENERGY_COST
                elif event.key == K_b:
                    self.mob_manager.shoot_bullet(self.player.absolute_shoot_point())
                    self.player.energy -= BULLET_ENERGY_COST
                    self.play_sound(SOUND_BULLET)
                elif event.key == K_RIGHT or event.key == K_d:
                    self.user_presses_right = True
                elif event.key == K_LEFT or event.key == K_a:
                    self.user_presses_left = True
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    self.user_presses_right = False
                elif event.key == K_LEFT or event.key == K_a:
                    self.user_presses_left = False

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.floor, self.floor_coordinates())

        self.player.render(self.screen, self.x_scroll)
        self.mob_manager.render(self.screen, self.x_scroll)
        # self.mob_manager.show_aabbs(self.screen, self.x_scroll)
        self.texts.render(self.screen, self.x_scroll)

        pygame.display.flip()
        self.frame_duration_ms = self.clock.tick_busy_loop()

    def main_loop(self):
        while self.running:
            self.handle_events()

            self.player_acceleration()
            self.player.gravity(self.frame_duration_ms)
            self.player.move(self.frame_duration_ms)
            self.mob_manager.move(self.frame_duration_ms, self)
            self.texts.move(self.frame_duration_ms)
            self.manage_scroll()

            if self.player.x > WORLD_SIZE + 2000 - SCREEN_WIDTH - 270:
                self.running = False
                self.game_state = GAME_WON

            self.mob_manager.interact(self)
            self.mob_manager.antibody_cleanup(self.x_scroll)
            self.mob_manager.bullet_cleanup(self.x_scroll)
            self.mob_manager.enemy_bullet_cleanup(self.x_scroll)

            self.render()

    def player_acceleration(self):
        if self.user_presses_left == self.user_presses_right:
            self.player.dx = 0
            return
        if self.user_presses_right:
            self.player.dx = PLAYER_SPEED
        else:
            self.player.dx = -PLAYER_SPEED

    def floor_coordinates(self):
        if self.player.dx >= 0:
            if self.x_scroll < WORLD_SIZE:
                if self.x_scroll - self.floor_shift >= self.floor.get_width() - SCREEN_WIDTH:
                    self.floor_shift += self.floor.get_width() - SCREEN_WIDTH
        else:
            if self.x_scroll - self.floor_shift <= 0:
                self.floor_shift -= self.floor.get_width() - SCREEN_WIDTH
        return (0-self.x_scroll + self.floor_shift, SCREEN_HEIGHT - self.floor.get_height())

    def manage_scroll(self):
        if self.player.dx >= 0:
            if self.player.x - self.x_scroll > POSITIVE_SCROLL_THRESHOLD:
                self.x_scroll = self.player.x - POSITIVE_SCROLL_THRESHOLD
        else:
            if self.player.x - self.x_scroll < NEGATIVE_SCROLL_THRESHOLD:
                self.x_scroll = self.player.x - NEGATIVE_SCROLL_THRESHOLD
        if pygame.time.get_ticks() - self.last_time_completion_indicaiton > COMPLETION_INDICATION_PERIOD:
            self.texts.add_text(str(int(self.x_scroll*100/WORLD_SIZE))+"% Complete", 40, WHITE, [int(self.player.x+240), 300], [0, -0.07], 2800)
            self.texts.add_text("time : " + str(int((pygame.time.get_ticks() - self.start_time)/10)/100.0)+" seconds", 40, WHITE, [int(self.player.x+200), 330], [0, -0.063], 2800)
            self.last_time_completion_indicaiton = pygame.time.get_ticks()

    def game_over(self):
        self.running = False
        self.game_state = GAME_OVER

    def play_sound(self, sound_id):
        self.sounds[sound_id].play()