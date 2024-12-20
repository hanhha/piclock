#!/usr/bin/env python

import pygame
from datetime import datetime as date
import math
import helper

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

shift     = 0
shift_dir = False

def draw_screen (screen, fcst_weather = None):
    """Draw a screen with weather information"""
    global shift, shift_dir

    SCR_W    = screen.get_width()  - 5
    SCR_H    = screen.get_height() - 5
    MARGIN_H = MARGIN_W = 5 # margin of analog clock from window border

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    weather_font   = pygame.font.SysFont ('Calibri', int((SCR_H / 7)*0.6), False, False)
    row_h          = (SCR_H - 2*MARGIN_H) / 7
    char_w, char_h = weather_font.size("a")

    tbl     = [['' for c in range(5)] for r in range(7)]
    max_len = [0 for c in range(5)]

    for i in range(len(fcst_weather)):
        tbl [i][0] = date.strptime(fcst_weather[i]['datetime'], "%Y-%m-%d").date().strftime("%a") if i > 0 else "Today"
        tbl [i][1] = 'Fl: '    + str(fcst_weather[i]['feelslike']) + '°C'
        tbl [i][2] = 'H: '     + str(fcst_weather[i]['humidity']) + '%'
        tbl [i][3] = 'Cloud: ' + str(fcst_weather[i]['cloudcover']) + '%'
        tbl [i][4] = fcst_weather[i]['conditions']

        if max_len [0] < len (tbl [i][0]): max_len [0] = len (tbl [i][0])
        if max_len [1] < len (tbl [i][1]): max_len [1] = len (tbl [i][1])
        if max_len [2] < len (tbl [i][2]): max_len [2] = len (tbl [i][2])
        if max_len [3] < len (tbl [i][3]): max_len [3] = len (tbl [i][3])
        if max_len [4] < len (tbl [i][4]): max_len [4] = len (tbl [i][4])

    for r in range(7):
        for c in range(5):
            text = weather_font.render(tbl [r][c], True, WHITE)
            screen.blit (text, [MARGIN_W + sum(max_len[:c])*char_w + shift*char_w, MARGIN_H + r*row_h + (row_h - char_h)/2])
        if r > 0:
            pygame.draw.line (screen, YELLOW, [0, MARGIN_H + r*row_h], [SCR_W, MARGIN_H + r*row_h], 2)

    max_shift = sum (max_len) - ((SCR_W - MARGIN_W) / char_w)
    if max_shift <= 0:
        shift = 0
    else:
        shift = shift - 0.05 if not shift_dir else shift + 0.05
        if shift <= (0-max_shift) or shift >= 1:
            shift_dir = not shift_dir
