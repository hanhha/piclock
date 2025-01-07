#!/usr/bin/env python

import pygame
import os, random
from config import digiframe_dir

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

img = None

def draw_screen (screen, change = False):
    """Draw a screen with new randomized photo if change == True"""
    global img

    SCR_W    = screen.get_width()  - 5
    SCR_H    = screen.get_height() - 5
    MARGIN_H = MARGIN_W = 5 # margin of analog clock from window border

    if change:
        try:
            filename = random.choice(os.listdir(digiframe_dir))
        except:
            filename = None

        if filename is not None:
            path = os.path.join(digiframe_dir, filename)
            try:
                img = pygame.image.load(path)
            except:
                img = None

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)
    if img is not None:
        img = pygame.transform.scale(img, [SCR_W, SCR_H])
        screen.blit (img, [MARGIN_W, MARGIN_H])
