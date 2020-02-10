import pygame
from pyganim import PygAnimation
from math import sin, cos, radians, atan, pi

from data.Camera import Camera
from data.Entity import Entity


class Ship(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('data/img/lander0.png').convert_alpha()
        self.second_stage = False


        img = pygame.image.load('data/img/fire.png').convert_alpha()
        self.fire = PygAnimation([[img.subsurface(img.get_width() // 10 * x, img.get_height() // 6 * y,
                                                  img.get_width() // 10, img.get_height() // 6), 10]
                                  for y in range(0, 6) for x in range(0, 10)])
        self.fire.play()

        self.rcs = PygAnimation([[
            pygame.transform.scale(img.subsurface(img.get_width() // 10 * x, img.get_height() // 6 * y, 
                img.get_width() // 10, img.get_height() // 6), (10, 10)), 10]
                                  for y in range(0, 6) for x in range(0, 10)])
        self.rcs.play()
        self.rcsMode = 0
    
    def draw(self, window):
        if self.up and (self.fuel > 0):
            img = pygame.transform.rotate(self.fire.getCurrentFrame(), 270 - self.angle)
            window.blit(
                img, 
                Camera.get_pos(
                    self.x - img.get_width() / 2 - 25 * cos(radians(self.angle)),
                    self.y - img.get_height() / 2 - 25 * sin(radians(self.angle))
                )
            )
        if self.left or self.right:
            if self.left:
                img = pygame.transform.rotate(self.rcs.getCurrentFrame(), -self.angle)
                x = self.x - img.get_width() / 2 + 12 * cos(radians(self.angle + 90))
                y = self.y - img.get_height() / 2 + 12 * sin(radians(self.angle + 90))
                x += 2.5 * cos(radians(self.angle))
                y += 2.5 * sin(radians(self.angle))
            elif self.right:
                img = pygame.transform.rotate(self.rcs.getCurrentFrame(), 180 - self.angle)
                x = self.x - img.get_width() / 2 + 12 * cos(radians(self.angle - 90))
                y = self.y - img.get_height() / 2 + 12 * sin(radians(self.angle - 90))
                x += 5 * cos(radians(self.angle))
                y += 5 * sin(radians(self.angle))
            window.blit(img, Camera.get_pos(x, y))

        img = pygame.transform.rotate(self.image, 270 - self.angle)
        pygame.draw.line(
            window, 
            (255, 0, 255), 
            Camera.get_pos(self.x, self.y),
            Camera.get_pos(self.x + self.dx * 5, self.y + self.dy * 5)
        )
        window.blit(
            img, 
            Camera.get_pos(self.x - img.get_width() / 2, self.y - img.get_height() / 2)
        )

    def render(self):
        def getSpeedAngle():
            if self.dx == 0:
                if self.dy > 0:
                    return pi / 2
                else:
                    return pi / 2 * 3
            elif self.dx < 0:
                return pi + atan(self.dy / self.dx)
            elif self.dx > 0 and self.dy > 0:
                return atan(self.dy / self.dx)
            elif self.dx > 0:
                return atan(self.dy / self.dx) + pi * 2

        def distance(a, b):
            r1 = a - b
            if r1 > pi:
                return 2 * pi - r1
            elif r1 < -pi:
                return 2 * pi - r1
            return r1

        # RCS Mode
        if self.rcsMode == 1:
            # Stabilization
            self.left = self.right = False
            if self.da > .1:
                self.left = True
            elif self.da < -.1:
                self.right = True
            else:
                if abs(self.da) < .8:
                    self.da = 0
        elif self.rcsMode == 2:
            # Prograde
            self.left = self.right = False
            sA = getSpeedAngle()
            aA = radians(self.angle)
            diff = distance(sA, aA)
            if diff < -.1:
                if self.da > -1:
                    self.left = True
            elif diff > .1:
                if self.da < 1:
                    self.right = True
            else:
                if abs(self.da) < 1:
                    self.da = 0
        elif self.rcsMode == 3:
            # Retrograde
            self.left = self.right = False
            sA = getSpeedAngle() + pi
            aA = radians(self.angle)
            diff = distance(sA, aA)
            if diff < -.1:
                if self.da > -1:
                    self.left = True
            elif diff > .1:
                if self.da < 1:
                    self.right = True
            else:
                if abs(self.da) < 1:
                    self.da = 0


        super().render()
