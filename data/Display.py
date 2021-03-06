import pygame
from math import cos, sin, radians, sqrt, pi, degrees

from data.settings import D_SIZE, F_SIZE
from data.Ship import Ship


def displayDraw(display, ship, font, mapp, aim):
    d = pygame.Surface([D_SIZE[0] * 2, D_SIZE[1] * 2])
    d.fill((0, 0, 0))

    # Planet drawing
    for i, le in enumerate(mapp):
        angle = i / len(mapp) * 2 * pi
        d.set_at(
            (
                round(D_SIZE[0] + le * cos(angle) / F_SIZE[0] * D_SIZE[0]),
                round(D_SIZE[1] + le * sin(angle) / F_SIZE[1] * D_SIZE[1])
            ),
            (255, 255, 255)
        )

    # Aim drawing
    le = mapp[round(aim / 2 / pi * len(mapp))]
    pygame.draw.circle(
        d,
        (255, 0, 255),
        (
            round(D_SIZE[0] + le * cos(aim) / F_SIZE[0] * D_SIZE[0]),
            round(D_SIZE[1] + le * sin(aim) / F_SIZE[1] * D_SIZE[1])
        ),
        3
    )

    # Trace
    for i in range(1, len(ship.trace['points'])):
        p1 = ship.trace['points'][i - 1]
        p2 = ship.trace['points'][i]
        pygame.draw.line(
            d,
            (100, 100, 100),
            (
                round(p1[0] * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
                round(p1[1] * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
            ),
            (
                round(p2[0] * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
                round(p2[1] * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
            ),
        )

    # Apogee and perigee
    if ship.trace['apogee']:
        pygame.draw.circle(
            d, 
            (255, 0, 0), 
            (
                round(ship.trace['apogee'][0] * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
                round(ship.trace['apogee'][1] * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
            ),
            1
        ) 
    if ship.trace['perigee']:
        pygame.draw.circle(
            d, 
            (0, 0, 255), 
            (
                round(ship.trace['perigee'][0] * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
                round(ship.trace['perigee'][1] * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
            ),
            1
        )


    # Heading line
    pygame.draw.line(
        d, 
        (255, 0, 0),
        (
            round(ship.x * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
            round(ship.y * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
        ),
        (
            round(ship.x * D_SIZE[0] / F_SIZE[0] + cos(radians(ship.angle)) * 10 + D_SIZE[0] / 2), 
            round(ship.y * D_SIZE[1] / F_SIZE[1] + sin(radians(ship.angle)) * 10 + D_SIZE[1] / 2)
        )
    )

    # Speed line
    pygame.draw.line(
        d, 
        (200, 200, 200),
        (
            round(ship.x * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2),
            round(ship.y * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
        ),
        (
            round(ship.x * D_SIZE[0] / F_SIZE[0] + ship.dx + D_SIZE[0] / 2),
            round(ship.y * D_SIZE[1] / F_SIZE[1] + ship.dy + D_SIZE[1] / 2)
        )
    )

    # Ship position circle
    pygame.draw.circle(
        d, 
        (255, 100, 100), 
        (
            round(ship.x * D_SIZE[0] / F_SIZE[0] + D_SIZE[0] / 2), 
            round(ship.y * D_SIZE[1] / F_SIZE[1] + D_SIZE[1] / 2)
        ),
        2
    )

    # Rotating
    d = pygame.transform.rotate(d, degrees(ship.planetAngle) + 90)
    display.fill((0, 0, 0))
    display.blit(d, (D_SIZE[0] / 2 - d.get_width() / 2, D_SIZE[1] / 2 - d.get_height() / 2))
    
    # Height / Speed information
    display.blit(
        font.render(
            '{} {}'.format(
                round(sqrt(pow(ship.x - 6000, 2) + pow(ship.y - 6000, 2)) - mapp[round(ship.planetAngle / 2 / pi * len(mapp))] - 6), 
                round(sqrt(pow(ship.dx, 2) + pow(ship.dy, 2)))
            ),
            False,
            (100, 100, 100)
        ), 
    (3, 3)
    )

    # Fuel information
    display.blit(font.render('{}'.format(round(ship.fuel)), False, (100, 100, 100)), (3, 13))
    
    # Border
    pygame.draw.rect(display, (100, 100, 100), (0, 0, D_SIZE[0], D_SIZE[1]), 2)
