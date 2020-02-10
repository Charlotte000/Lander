import pygame
from math import sin, cos, pi, sqrt, asin, degrees, radians
from datetime import datetime
from random import uniform

from data.settings import SIZE, D_SIZE, F_SIZE, mapp, explode
from data.Display import displayDraw

from data.Ship import Ship
from data.Camera import Camera
from data.Human import Human
from data.Trash import Trash


def key_event(player):
    global isHuman, trash
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.left = True
            if event.key == pygame.K_d:
                player.right = True
            if event.key == pygame.K_w:
                player.up = True
            if event.key == pygame.K_r:
                player.left = player.right = player.up = False
            if event.key == pygame.K_SPACE and not isHuman and not player.second_stage:
                player.image = pygame.image.load('data/img/lander2.png').convert_alpha()
                player.fuel = 100
                player.second_stage = True

                i = pygame.image.load('data/img/lander1.png').convert_alpha()
                tr = Trash(player.x, player.y, i)
                tr.angle = player.angle
                tr.dx, tr.dy, tr.da = player.dx, player.dy, player.da
                tr.dx -= .5 * cos(radians(tr.angle))
                tr.dy -= .5 * sin(radians(tr.angle))
                trash.append(tr)
            if event.key == pygame.K_RETURN and player.dx == 0 and player.dy == 0:
                isHuman = not isHuman
                if isHuman:
                    human.x, human.y = ship.x, ship.y
                    human.dx, human.dy, human.da = ship.dx, ship.dy, ship.da
            if event.key == pygame.K_KP0:
                if not isHuman:
                    player.rcsMode = 0
                    player.left = player.right = False
            if event.key == pygame.K_KP1:
                if not isHuman:
                    player.rcsMode = 1
            if event.key == pygame.K_KP2:
                if not isHuman:
                    player.rcsMode = 2
            if event.key == pygame.K_KP3:
                if not isHuman:
                    player.rcsMode = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.left = False
            if event.key == pygame.K_d:
                player.right = False
            if event.key == pygame.K_w:
                player.up = False


pygame.font.init()
font = pygame.font.Font(None, 18)

window = pygame.display.set_mode(SIZE)
display = pygame.Surface(D_SIZE)
screen = pygame.Surface(SIZE)

ship = Ship(6000, 3000 - 2000)
ship.dx = 10
human = Human(0, 0)
isHuman = False
trash = []

aim = pi / 2 + uniform(-pi / 6, pi / 6)

map_img = pygame.Surface(F_SIZE)
for i, le in enumerate(mapp[:-1]):
    angle = i / len(mapp) * 2 * pi
    angle2 = (i + 1) / len(mapp) * 2 * pi
    le2 = mapp[i + 1]
    pygame.draw.line(
        map_img, 
        (255, 255, 255),
        (round(F_SIZE[0] / 2 + le * cos(angle)), round(F_SIZE[1] / 2 + le * sin(angle))),
        (round(F_SIZE[0] / 2 + le2 * cos(angle2)), round(F_SIZE[1] / 2 + le2 * sin(angle2)))
    )

        
while True:
    t = datetime.now()

    if isHuman:
        key_event(human)
    else:
        key_event(ship)

    # Rendering
    if isHuman:
        Camera.render(human.x, human.y)
        human.render()
    else:
        Camera.render(ship.x, ship.y)
    ship.render()
    for tr in trash:
        tr.render()

    # =GAMING SCREEN=
    screen.fill((0, 0, 0))
    screen.blit(map_img, Camera.get_pos(0, 0, True))

    ship.draw(screen)
    if isHuman:
        human.draw(screen)
    for tr in trash:
        tr.draw(screen)

    # Aim landing position circle
    le = mapp[round(aim / 2 / pi * len(mapp))]
    pygame.draw.circle(
        screen, 
        (255, 0, 255), 
        Camera.get_pos(
            F_SIZE[0] / 2 + le * cos(aim),
            F_SIZE[1] / 2 + le * sin(aim),
            True
        ), 
        5
    )
    
    # Explosion
    if ship.to_explode:
        explode.blit(screen, Camera.get_pos(ship.x - 64, ship.y - 64))
        if explode.numFrames == explode.currentFrameNum + 1:
            ship.to_explode = False

    for tr in trash:
        if tr.to_explode:
            explode.blit(screen, Camera.get_pos(tr.x - 64, tr.y - 64))
            if explode.numFrames == explode.currentFrameNum + 1:
                tr.to_explode = False

    if isHuman:
        sI = pygame.transform.rotate(screen, degrees(human.planetAngle) + 90)
    else:
        sI = pygame.transform.rotate(screen, degrees(ship.planetAngle) + 90)

    # Fuel indicator
    pygame.draw.rect(
        sI, 
        (100, 100, 100), 
        (sI.get_width() // 2 - 15, sI.get_height() // 2 - 40, int(ship.fuel // 2), 10)
    )
    pygame.draw.rect(
        sI, 
        (200, 200, 200), 
        (sI.get_width() // 2 - 15, sI.get_height() // 2 - 40, 50, 10),
        1
    )
    # ===GAMING SCREEN===

    # Display
    if isHuman:
        displayDraw(display, human, font, mapp, aim)
    else:
        displayDraw(display, ship, font, mapp, aim)

    # Drawing of window
    window.fill((0, 0, 0))
    window.blit(sI, (SIZE[0] // 2 - sI.get_width() // 2, SIZE[1] // 2 - sI.get_height() // 2))
    window.blit(display, (0, SIZE[1] - D_SIZE[1]))

    # FPS
    window.blit(
        font.render(
            f'{round(1000000 / (datetime.now() - t).microseconds)}',
            False,
            (100, 100, 100)
        ),
        (3, 3)
    )

    # Window update
    pygame.display.flip()
    pygame.time.Clock().tick(60)
