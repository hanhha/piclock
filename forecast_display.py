#!/usr/bin/env python

import pygame
from datetime import datetime as date
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

def draw_screen (screen, fcst_weather = None):
    """Draw a screen with weather information"""

    SCR_W    = screen.get_width()  - 5
    SCR_H    = screen.get_height() - 5
    MARGIN_H = MARGIN_W = 5 # margin of analog clock from window border

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    weather_font = pygame.font.SysFont ('Calibri', int((SCR_H / 7)*0.8), False, False)
    row_h        = (SCR_H - 2*MARGIN_H) / 7

    for i in range(len(fcst_weather)):
        text = weather_font.render(date.strptime(fcst_weather[i]['datetime'], "%Y-%m-%d").date().strftime("%a") if i > 0 else "Today", True, WHITE)
        screen.blit (text, [MARGIN_W, MARGIN_H + i*row_h])
