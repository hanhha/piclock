#!/usr/bin/env python

import pygame, thorpy as tp
from datetime import datetime
import math, os

has_button = False
try:
    from gpiozero import Button
    has_button = True
except ImportError as err:
    has_button = False

import helper
import clock_display as scr1
import forecast_display as scr2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

CLOCK_SCR   = 0
WEATHER_SCR = 1
CONTROL_SCR = 2

location     = helper.get_loc_name ()
selected_scr = CLOCK_SCR
old_scr      = selected_scr

def on_switch_released ():
    """Action when clock button released"""
    global selected_scr
    selected_scr = CLOCK_SCR if selected_scr == CONTROL_SCR else CONTROL_SCR
    #print ("Key 1 was clicked, switched to other screen.")

def on_weather_pressed ():
    """Action when weather button pressed"""
    global selected_scr
    global old_scr
    old_scr = selected_scr
    selected_scr = WEATHER_SCR
    scr2.shift = 0
    scr2.shift_dir = False
    #print ("Key 2 was clicked, switched to WEATHER screen.")

def on_weather_released ():
    """Action when weather button released"""
    global selected_scr
    global old_scr
    selected_scr = old_scr 
    #print ("Key 2 was clicked, switched to old screen.")

def on_control_released ():
    """Action when control button released"""
    global selected_scr, has_button

    if has_button:
        os.system ("sudo reboot")
    else:
        print ("Key 3 was clicked.")

pihole_sts = True

if has_button:
    Clock_btn   = Button (pin = 18, pull_up = True) # GPIO18 for KEY_1
    Clock_btn.when_released = on_switch_released
    Weather_btn = Button (pin = 23, pull_up = True) # GPIO23 for KEY_2
    Weather_btn.when_released = on_weather_released
    Weather_btn.when_pressed = on_weather_pressed
    Control_btn = Button (pin = 24, pull_up = True) # GPIO24 for KEY_3
    Control_btn.when_released = on_control_released

def draw_weather_screen (screen, weather = None):
    """Draw a screen with weather information"""

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(WHITE)

# setup
pygame.init()
screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
pygame.display.set_caption ('Clock')
pygame.mouse.set_visible (False)
need_update_weather = pygame.USEREVENT + 1
pygame.time.set_timer(need_update_weather, 3600000)  # 1h = 60m = 3600s = 3600000 milliseconds - set to query weather every 1H
tp.set_default_font ('Calibri', 50)
tp.init(screen, tp.theme_game1) #bind screen to gui elements and set theme
clock = pygame.time.Clock ()

# UI for control screen
pihole_btn = tp.SwitchButtonWithText ("Pihole", ("On", "Off"), value = 0, size = (100, 50))
ctrl_ui    = tp.Group ([pihole_btn])
ui_upd     = ctrl_ui.get_updater ()

cur_weather, fcst_weather = helper.query_weather ()

def draw_control_screen (screen, events):
    """Draw a screen with control buttons"""
    global pihole_sts

    # Handle Pihole button
    if (True if pihole_btn.get_value() == "On" else False) != pihole_sts:
        helper.toggle_pihole (not pihole_sts)
        pihole_sts = not pihole_sts

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)
    ui_upd.update (events = events)

running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_2:
                on_weather_pressed ()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                on_switch_released ()
            elif event.key == pygame.K_2:
                on_weather_released ()
            if event.key == pygame.K_3:
                on_control_released ()
        elif event.type == need_update_weather:
            cur_weather, tmp_fcst_weather = helper.query_weather ()
            fcst_weather = tmp_fcst_weather if tmp_fcst_weather is not None else fcst_weather

    if selected_scr == CLOCK_SCR:
        scr1.draw_screen (screen, cur_weather, location)
    elif selected_scr == WEATHER_SCR:
        scr2.draw_screen (screen, fcst_weather)
    elif selected_scr == CONTROL_SCR:
        draw_control_screen (screen, events)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit ()
