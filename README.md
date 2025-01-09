# piclock

Just another RPi Clock to keep spare parts running. It can show a clock, some weather forecast information, or digital frame, control some stuffs.
![Clock on desktop](https://github.com/user-attachments/assets/da1a707f-f2b4-4e64-8725-7a9e910c99b8)

## Requirements:
### Hardware:
- Raspberry 2B.
- Waveshare 3.2" LCD with resistive touch.

3d print models for the case and buttons: https://www.thingiverse.com/thing:6906189

### Software libraries:
- Python3
- Pygame (https://www.pygame.org)
- reverse_geocode (https://github.com/richardpenman/reverse_geocode)
- gpiozero (https://gpiozero.readthedocs.io/en/stable/index.html)
- thorpy (https://www.thorpy.org/)

## Features:
- Use https://www.visualcrossing.com to get weather data. It will fetch once per hour so that no cost.
- Show pictures in folder synced with Google Photos (https://www.thedigitalpictureframe.com/how-to-synchronize-your-digital-picture-frame-with-your-google-photos-albums-using-rclone/).

## Usage:
- Create config.py file in same folder with info of location, API key and other user informations, i.e:
<blockquote>
  latitude        = "10"
  
  longitude       = "10"
  
  visualcross_key = "7U83WAY93XSG6XCMRZD"
  
  pihole_url = "http://192.168.1.2"
  
  pihole_key ="33356c13a1389823ec782b1d1f8b4be"
  
  digiframe_dir = "/home/pi/Pictures/digitalframe"
</blockquote>

- Click button 1 to rotate between clock, digital frame and control screens.
- Keep pressing button 2 to show weather forecast in 7 days.
