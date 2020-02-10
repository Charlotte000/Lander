from settings import F_SIZE, mapp
from math import sqrt, degrees, atan, sin, cos

from data.Ship import Ship


class AutoPilot:
    def __init__(self, pilot_ship):
        self.ship = pilot_ship
        self.islanded = True
        self.lenght = 0
        self.land = [0, 0]

    def init_pilot(self):
        ship = Ship(self.ship.x, self.ship.y)
        ship.dx, ship.dy = self.ship.dx, self.ship.dy
        ship.angle = self.ship.angle
        for count in range(0, 1000):
            ship.applyGravity()
            if ship.collision():
                self.land = [ship.x, ship.y]
                break
            ship.move()

        dxy = sqrt(pow(ship.dx, 2) + pow(ship.dy, 2))
        time = dxy / Ship.thrust
        self.lenght = dxy * time - (Ship.thrust * pow(time, 2)) / 2 + 50

    def render(self):
        if not self.islanded:
            self.init_pilot()
            if self.ship.dx != 0:
                dxdy_angle = degrees(atan(self.ship.dy / self.ship.dx))
                if dxdy_angle > 0:
                    dxdy_angle -= 180
                self.ship.left = self.ship.right = self.ship.up = False
                if self.ship.angle > dxdy_angle:
                    self.ship.left = True
                if self.ship.angle < dxdy_angle:
                    self.ship.right = True
            if sqrt(pow(self.land[0] - self.ship.x, 2) + pow(self.land[1] - self.ship.y, 2)) < self.lenght:
                if sqrt(pow(self.ship.dx, 2) + pow(self.ship.dy, 2)) >= 0.5:
                    self.ship.up = True
            if self.ship.dx == self.ship.dy == 0:
                self.islanded = True
                self.ship.left = self.ship.right = self.ship.up = False