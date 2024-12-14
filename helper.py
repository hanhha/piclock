#!/usr/bin/env python3

import pygame
import urllib.request, json
from config import latitude, longitude, key

def query_weather ():
    """Query weather information from visualcrossing.com"""
    jsonData = None

    try:
        ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude}%2C{longitude}?unitGroup=metric&include=current&key={key}&contentType=json")
        # Parse the results as JSON
        jsonData = json.load(ResultBytes)
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode()
        print('Error code: ', e.code,ErrorInfo)

    if jsonData:
        return jsonData ['currentConditions'], jsonData ['days']
    else:
        return None, None