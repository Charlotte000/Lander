import pygame
from pyganim import PygAnimation
from math import sin, cos, radians, pi

from data.Camera import Camera
from data.Entity import Entity
from data.settings import mapp, F_SIZE


class Human(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('data/img/astronaut.png').convert_alpha()
        self.direction = -1

    def keyEvent(self):
        self.fuel = 100
        if self.left or self.right:
            if self.left:
                self.direction = -1
                a0 = self.planetAngle - .001
            elif self.right:
                self.direction = 1
                a0 = self.planetAngle + .001
            length = mapp[round((a0) / 2 / pi * len(mapp))] + self.image.get_height() / 2
            x, y = F_SIZE[0] / 2 + length * cos(a0), F_SIZE[1] / 2 + length * sin(a0)
            self.x += (x - self.x) / 5
            self.y += (y - self.y) / 5
    
    def draw(self, window):
        img = self.image.copy()
        if self.direction == -1:
            img = pygame.transform.flip(img, True, False)
        img = pygame.transform.rotate(img, 270 - self.angle)
        window.blit(
            img, 
            Camera.get_pos(self.x - img.get_width() // 2, self.y - img.get_height() // 2)
        )
