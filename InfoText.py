import pygame
from pygame.locals import *
from constants import *

class InfoText:
    """This class will be used to display short and temporary textual information (eg -42 point...)"""

    def __init__(self, font):
        self.font = font
        self.texts = list()

    def add_text(self, text, size, color, pos, speed, fadeout):
        self.texts.append([text, size, color, pos, speed, fadeout, fadeout])

    def move(self, time):
        text_deletion_list = list()
        updated_list = list()
        for i, text in enumerate(self.texts):
            text[POS][X] += text[SPEED][X] * time
            text[POS][Y] += text[SPEED][Y] * time
            text[FADEOUT] -= time
            if text[FADEOUT] < 0:
                text_deletion_list.append(i)
        for i in range(len(self.texts)):
            if i not in text_deletion_list:
                updated_list.append(self.texts[i])
        self.texts = updated_list

    def render(self, screen, x_scroll):
        for text in self.texts:
            surface = self.font.render(text[TEXT], 0, text[COLOR], TRANSPARENT_COLOR)
            s = pygame.Surface((surface.get_width(), surface.get_height()), SRCCOLORKEY)
            s.set_colorkey(TRANSPARENT_COLOR)
            s.blit(surface, (0, 0))
            s.set_alpha((text[FADEOUT]*255.0)/text[DURATION])
            screen.blit(s, (text[POS][X] - x_scroll, text[POS][Y]))