import pygame
from pygame.locals import *
from constants import *
from Game import *

class Intro:
    """this class begins and ends the game"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Screen Bacteria - Ludum Dare 31 Entry")
        self.slides = list()
        self.slides.append(pygame.image.load("intro-0.png").convert())
        self.screen.blit(self.slides[0], (0,0))
        for i in range(1, 10):
            self.slides.append(pygame.image.load("intro-"+str(i)+".png").convert())
        pygame.display.flip()

        self.g = None
        self.running = True
        self.greetings()
        pygame.quit()

    def greetings(self):
        self.intro()
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    else:
                        self.run()

    def run(self):
        self.g = Game(self.screen)
        if self.g.game_state == GAME_OVER:
            self.g.screen.blit(pygame.font.Font("font.ttf", 80).render("GAME OVER", 1, (255, 42, 24)), (10,150))
        elif self.g.game_state == GAME_WON:
            self.g.screen.blit(pygame.font.Font("font.ttf", 80).render("YOU WON", 1, (42, 255, 24)), (90,150))
        self.g.screen.blit(pygame.font.Font("font.ttf", 30).render("Press any key to play again", 1, WHITE), (10,SCREEN_HEIGHT - 100))
        pygame.display.flip()
        pygame.time.delay(500)
        self.g.play_sound(SOUND_END)
        pygame.event.clear()

    def intro(self):
        slide = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    else:
                        slide += 1
                        if len(self.slides) == slide:
                            self.run()
                            return
                        self.screen.blit((self.slides[slide]), (0,0))
                        pygame.display.flip()

if __name__ == "__main__":
    ludum_dare = Intro()