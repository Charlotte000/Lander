import pygame
from pyganim import PygAnimation
from math import sin, cos, radians

from data.Camera import Camera
from data.Entity import Entity


class Trash(Entity):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.image = img
    
    def draw(self, window):
        img = pygame.transform.rotate(self.image, 270 - self.angle)
        window.blit(
            img, 
            Camera.get_pos(self.x - img.get_width() // 2, self.y - img.get_height() // 2)
        )
