#!/usr/bin/env python3

import pygame
import urllib.request, json
import reverse_geocode
from config import latitude, longitude, visualcross_key, pihole_url, pihole_key

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

def query_weather ():
    """Query weather information from visualcrossing.com"""
    jsonData = None

    try:
        ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude}%2C{longitude}?unitGroup=metric&include=current&key={visualcross_key}&contentType=json")
        # Parse the results as JSON
        jsonData = json.load(ResultBytes)
    except urllib.error.HTTPError as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code,ErrorInfo)

    if jsonData:
        return jsonData ['currentConditions'], jsonData ['days'][:7]
    else:
        return None, None

def get_loc_name ():
    return reverse_geocode.get ((float(latitude), float(longitude)))

def toggle_pihole (status):
    try:
        ResultBytes = urllib.request.urlopen(f"{pihole_url}/admin/api.php?{'enable' if status else 'disable'}&auth={pihole_key}")
    except urllib.error.HTTPError as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code,ErrorInfo)

def rpad_str (org_str, l):
    """Right pad with spaces"""
    if l > len(org_str):
        return org_str + ' '*(l - len(org_str))
    else:
        return org_str[:l]

def lpad_str (org_str, l):
    """Right pad with spaces"""
    if l > len(org_str):
        return ' '*(l - len(org_str)) + org_str
    else:
        return org_str[-l:]

def draw_notice (screen, text):
    """Draw a screen with notice"""
    global shift, shift_dir

    SCR_W    = screen.get_width()  - 5
    SCR_H    = screen.get_height() - 5
    MARGIN_H = MARGIN_W = 5 # margin of analog clock from window border

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    font   = pygame.font.SysFont ('Calibri', int((SCR_H / 7)*0.6), False, False)

    txt = font.render(text, True, WHITE)
    screen.blit (txt, [MARGIN_W, MARGIN_H])
