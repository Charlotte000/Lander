import pygame
from pyganim import PygAnimation
from random import randint
from opensimplex import OpenSimplex
from math import pi, cos, sin


SIZE = [1000, 600]
F_SIZE = [12000, 12000]
D_SIZE = [200, 200]

pygame.display.set_mode(SIZE)

# Map generation
mapp = []
noiseGen = OpenSimplex()
off = [randint(0, 500), randint(0, 500)]
for i in range(1000):
	angle = i / 1000 * 2 * pi
	r = noiseGen.noise3d(off[0] + cos(angle) * 10, off[1] + sin(angle) * 10, 0) * 200 + 3000
	c = noiseGen.noise3d(off[0] + cos(angle) * 15, off[1] + sin(angle) * 15, 156)
	if c < 0:
		r += c * 200
	mapp.append(r)

# Explosion
img = pygame.image.load('data/img/explosion.png').convert_alpha()
explode = PygAnimation([[img.subsurface(img.get_width() // 4 * x, img.get_height() // 4 * y,
										  img.get_width() // 4, img.get_height() // 4), 100]
						  for y in range(0, 4) for x in range(0, 4)])
explode.play()
