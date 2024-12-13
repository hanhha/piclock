#!/usr/bin/env python

import pygame
from datetime import datetime
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def circle_point(center, radius, theta):
    """Calculates the location of a point of a circle given the circle's
       center and radius as well as the point's angle from the xx' axis"""

    return (center[0] + radius * math.cos(theta),
            center[1] + radius * math.sin(theta))

def line_at_angle(screen, center, radius, theta, color, width):
    """Draws a line from a center towards an angle. The angle is given in
       radians."""
    point = circle_point(center, radius, theta)
    pygame.draw.line(screen, color, center, point, width)

def get_angle(unit, total):
    """Calculates the angle, in radians, corresponding to a portion of the clock
       counting using the given units up to a given total and starting from 12
       o'clock and moving clock-wise."""
    return 2 * math.pi * unit / total - math.pi / 2

def draw_clock_screen (screen):
    """Draw a screen with analog and digital clocks"""

    DIGITAL_H = 100 # height of digital clock
    CLOCK_W = screen.get_width() - 5 # analog clock width
    CLOCK_H = screen.get_height() - 5 # analog clock heigmt
    MARGIN_H = MARGIN_W = 5 # margin of analog clock from window border
    CLOCK_R = (CLOCK_H - MARGIN_H) / 2 # clock radius
    HOUR_R = CLOCK_R / 2 # hour hand length
    MINUTE_R = CLOCK_R * 7 / 10 # minute hand length
    SECOND_R = CLOCK_R * 8 / 10 # second hand length
    TEXT_R = CLOCK_R * 9 / 10 # distance of hour markings from center
    TICK_R = 2 # stroke width of minute markings
    TICK_LENGTH = 5 # stroke length of minute markings
    HOUR_STROKE = 5 # hour hand stroke width
    MINUTE_STROKE = 2 # minute hand stroke width
    SECOND_STROKE = 2 # second hand stroke width
    CLOCK_STROKE = 2 # clock circle stroke width
    CENTER_W = 10 # clock center mount width
    CENTER_H = 10 # clock center mount height
    HOURS_IN_CLOCK = 12
    MINUTES_IN_HOUR = 60
    SECONDS_IN_MINUTE = 60

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    now = datetime.now()

    c_x, c_y = CLOCK_W / 2, CLOCK_H / 2
    center = (c_x, c_y)

     # draw clock
    pygame.draw.circle(
        screen,
        WHITE,
        center, CLOCK_H / 2 - MARGIN_H / 2,
        CLOCK_STROKE
    )

    # draw clock mount
    pygame.draw.circle(
        screen,
        WHITE,
        center, CENTER_H / 2 - MARGIN_H / 2,
        CLOCK_STROKE
    )

    # draw hands
    hour_theta = get_angle(now.hour + 1.0 * now.minute / MINUTES_IN_HOUR, HOURS_IN_CLOCK)
    minute_theta = get_angle(now.minute, MINUTES_IN_HOUR)
    second_theta = get_angle(now.second, SECONDS_IN_MINUTE)

    for (radius, theta, color, stroke) in (
        (HOUR_R, hour_theta, WHITE, HOUR_STROKE),
        (MINUTE_R, minute_theta, WHITE, MINUTE_STROKE),
        (SECOND_R, second_theta, RED, SECOND_STROKE),
    ):
        line_at_angle(screen, center, radius, theta, color, stroke)

    # draw hour markings (text)
    for hour in range(1, HOURS_IN_CLOCK + 1):
        theta = get_angle(hour, HOURS_IN_CLOCK)
        text = hour_font.render(str(hour), True, WHITE)
        screen.blit(text, circle_point(center, TEXT_R, theta))

    # draw minute markings (lines)
    for minute in range(0, MINUTES_IN_HOUR):
        theta = get_angle(minute, MINUTES_IN_HOUR)
        p1 = circle_point(center, CLOCK_R - TICK_LENGTH, theta)
        p2 = circle_point(center, CLOCK_R, theta)
        pygame.draw.line(screen, WHITE, p1, p2, TICK_R)

    # draw digital clock
    digital_text = now.strftime('%H:%M:%S')
    text = digital_font.render(digital_text, True, WHITE)
    screen.blit(
        text,
        [
            c_x - digital_font.size(digital_text)[0] / 2,
            c_y + CLOCK_R / 2 - DIGITAL_H / 2 - digital_font.size(digital_text)[1] / 2
        ]
    )

# setup
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Clock')
clock = pygame.time.Clock()
hour_font = pygame.font.SysFont('Calibri', 25, True, False)
digital_font = pygame.font.SysFont('Calibri', 32, False, False)
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_clock_screen (screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
