from math import sin, cos, sqrt, radians, asin, pi, degrees
import pygame

from data.settings import F_SIZE, mapp
from data.Camera import Camera


class Entity:
    gravity = 60
    thrust = .08
    f_burning = .245

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.dx = self.dy = self.da = 0
        self.fuel = 100
        self.left = self.right = self.up = False
        self.angle = -90
        self.planetAngle = 0
        self.to_explode = False
        self.trace = {'points': [], 'apogee': [], 'perigee': []}
        self.image = pygame.Surface((25, 25))

    def applyGravity(self):
        dx, dy = self.x - F_SIZE[0] / 2, self.y - F_SIZE[1]/ 2
        le = sqrt(pow(dx, 2) + pow(dy, 2))
        self.dx -= dx / le * Entity.gravity / pow(le, 2) * 9000
        self.dy -= dy / le * Entity.gravity / pow(le, 2) * 9000

    def collision(self):
        isFreeze = False
        dx, dy = self.x - F_SIZE[0] / 2, self.y - F_SIZE[1]/ 2
        le = sqrt(pow(dx, 2) + pow(dy, 2))
        if mapp[round(self.planetAngle / 2 / pi * len(mapp))] >= le - self.image.get_height() / 2:
            if not self.to_explode and sqrt(pow(self.dx, 2) + pow(self.dy, 2)) >= 1:
                self.to_explode = True
                self.fuel = 0
            self.dx = self.dy = 0
            self.angle = degrees(self.planetAngle)
            self.da = 0
            isFreeze = True
        if self.x - self.image.get_width() // 2 < 0:
            self.dx = 0
            self.x = self.image.get_width() // 2
            isFreeze = True
        elif self.x + self.image.get_width() // 2 > F_SIZE[0]:
            self.dx = 0
            self.x = F_SIZE[0] - self.image.get_width() // 2
            isFreeze = True

        if self.y - self.image.get_height() // 2 < 0:
            self.dy = 0
            self.y = self.image.get_height() // 2
            isFreeze = True
        elif self.y + self.image.get_height() // 2 > F_SIZE[1]:
            self.dy = 0
            self.y = F_SIZE[1] - self.image.get_height() // 2
            isFreeze = True
        return isFreeze

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.angle += self.da
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        dx, dy = self.x - F_SIZE[0] / 2, self.y - F_SIZE[1]/ 2
        le = sqrt(pow(dx, 2) + pow(dy, 2))
        self.planetAngle = asin((self.y - F_SIZE[1] / 2) / le)
        if dx < 0:
            self.planetAngle = pi - self.planetAngle

    def keyEvent(self):
        # Key event
        if self.left:
            self.da += -.1
        if self.right:
            self.da += .1
        if self.up and (self.fuel > 0):
            self.fuel -= Entity.f_burning
            self.dx += Entity.thrust * cos(radians(self.angle))
            self.dy += Entity.thrust * sin(radians(self.angle))

    def updateTrace(self):
        sh = Entity(self.x, self.y)
        sh.dx, sh.dy = self.dx, self.dy
        prevX, prevY = sh.x, sh.y
        isFreeze = False
        self.trace = {'points': [[prevX, prevY]], 'apogee': [], 'perigee': []}
        for _ in range(30):
            for _ in range(100):
                sh.applyGravity()
                if not isFreeze:
                    sh.move()
            isFreeze = sh.collision()

            # Apogee and perigee
            h = pow(sh.x - F_SIZE[0] / 2, 2) + pow(sh.y - F_SIZE[1] / 2, 2)
            if self.trace['perigee']:
                value = pow(self.trace['perigee'][0] - F_SIZE[0] / 2, 2) + pow(self.trace['perigee'][1] - F_SIZE[1] / 2, 2)
                if h < value:
                    self.trace['perigee'] = [sh.x, sh.y]
            else:
                self.trace['perigee'] = [sh.x, sh.y]
            if self.trace['apogee']:
                value = pow(self.trace['apogee'][0] - F_SIZE[0] / 2, 2) + pow(self.trace['apogee'][1] - F_SIZE[1] / 2, 2)
                if h > value:
                    self.trace['apogee'] = [sh.x, sh.y]
            else:
                self.trace['apogee'] = [sh.x, sh.y]

            self.trace['points'].append([prevX, prevY])
            prevX, prevY = sh.x, sh.y

    def render(self):
        self.applyGravity()
        self.collision()
        self.keyEvent()
        self.move()
        self.updateTrace()
