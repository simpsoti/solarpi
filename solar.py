#!/usr/bin/python3

from solardata import SolarData
from datetime import datetime, timezone
import pytz
from astral import Astral
import schedule
import time
import logging
from logging.handlers import RotatingFileHandler
import unicornhathd
import signal
import colorsys
from PIL import Image, ImageDraw, ImageFont
from pushover import init, Client
import json

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('solar.log', maxBytes=10*1024*1024, backupCount=5)
logger.addHandler(handler)

b = 0.4
unicornhathd.rotation(90)
unicornhathd.brightness(b)

energy_units = " kWh"
power_units = " kW"
push_energy = 0
push_power = 0

pushover_token = ""
pushover_userkey = ""
solaredge_apikey = ""
solaredge_siteid = ""
city_name = ""

with open('../config.json') as config_file:
    data = json.load(config_file)
    pushover_token = data['pushover_token']
    pushover_userkey = data['pushover_userkey']
    solaredge_apikey = data['solaredge_apikey']
    solaredge_siteid = data['solaredge_siteid']
    city_name = data['city_name']
    
init(pushover_token)

def TimeStamp():
    return datetime.today().strftime("%m/%d/%y %I:%M:%S %p")

def SendPushNotification():
    nl = "\n"
    today = "Energy: " + str(push_energy) + energy_units
    current = "Power: " + str(push_power) + power_units
    message = TimeStamp() + nl + today + nl + current
    logger.info("Push Notification:")
    logger.info(message)
    Client(pushover_userkey).send_message(message, title="Solar Production")
    
def SendErrorPushNotification():
    nl = "\n"
    error = "Production Error"
    current = "Power " + str(push_power) + power_units
    message = TimeStamp() + nl + error + nl + current
    logger.info("Push Notification - Error:")
    logger.info(message)
    Client(pushover_userkey).send_message(message, title="Solar Production Error")  


def OutputText(energy, power, r, g, b):
    today = "Energy: " + str(energy) + energy_units
    current = "Power: " + str(power) + power_units
    lines = [current, today]
    colours = (r, g, b)
    FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 10)
    width, height = unicornhathd.get_shape()
    text_x = width
    text_y = 2
    font_file, font_size = FONT
    font = ImageFont.truetype(font_file, font_size)
    text_width, text_height = width, 0

    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height, h)

    image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    offset_left = 0
    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, colours, font=font)
        offset_left += font.getsize(line)[0] + width

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y))
                red, green, blue = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, red, green, blue)

        unicornhathd.show()
        time.sleep(0.05)

def GetPixels(r, g, b):
    pixels = list([[[  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b]],

       [[  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0]],

       [[  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  r,   g,   b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [r, g, b],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0],
        [  0,   0,   0]]])
    return pixels


def DrawSun(r, g, b):
    pixels = GetPixels(r, g, b)
    for x in range(unicornhathd.WIDTH):
        for y in range(unicornhathd.HEIGHT):
            red, green, blue = pixels[x][y]
            unicornhathd.set_pixel(x, y, red, green, blue)
    unicornhathd.show()
    time.sleep(2.0)

def SunShining():
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    #logging.info(city)
    now = pytz.utc.localize(datetime.now())
    sun = city.sun(date=now, local=True)
    sunrise = sun['sunrise']
    sunset = sun['sunset']
    now_trunc = TruncateDateTime(now)
    sunrise_trunc = TruncateDateTime(sunrise)
    sunset_trunc = TruncateDateTime(sunset)
    shining = now_trunc > sunrise_trunc and now_trunc < sunset_trunc

    return shining, city, sunrise_trunc, sunset_trunc, now_trunc

def TruncateDateTime(dt):
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

def LogSun(city, sunrise, sunset, now):
    logger.info("Location: " + str(city))
    logger.info("Sunrise: " + str(sunrise))
    logger.info("Sunset: " + str(sunset))


def GetSolarData():
    logger.info("Getting solar data")
    solarData = SolarData(solaredge_apikey, solaredge_siteid)
    energy = solarData.last_day_energy()
    power = solarData.current_power()
    logger.info("Lifetime energy produced is " + str(solarData.lifetime_energy()) + energy_units)
    logger.info("Energy produced this year is " + str(solarData.last_year_energy()) + energy_units)
    logger.info("Energy produced today is " + str(energy) + energy_units)
    now = pytz.utc.localize(datetime.now())
    now_trunc = TruncateDateTime(now)
    logger.info(str(now_trunc) + " - Current power is " + str(power) + power_units)
    return energy, power

def GetColor(power):
    r = 0
    g = 0
    b = 0
    if power == 0:#blue
        r = 0
        g = 0
        b = 255
    elif power > 0 and power < 2:#purple
        r = 128
        g = 0
        b = 128
    elif power >= 2 and power < 4:#red
        r = 255
        g = 0
        b = 0
    elif power >= 4 and power < 5: #orange
        r = 255
        g = 165
        b = 0
    else: #yellow
        r = 255
        g = 255
        b = 0
    return r, g, b

def ProcessSolar(getData, energy, power, r, g, b):
    shining, city, sunrise, sunset, now = SunShining()
    global push_energy
    global push_power 
    if getData:
        LogSun(city, sunrise, sunset, now)
        energy, power = solarDataJob.run()
        r, g, b = GetColor(power)

    if shining:
        DrawSun(r, g, b)
        if pushNotificationJob.should_run:
            push_energy = energy
            push_power = power
            #print(str(push_energy) + " " + str(push_power))
            pushNotificationJob.run()
    elif power > 0:
        logger.info("Clean up edge case where power not zero very close to sunset.")
        logger.info("Edge Case Power: " + str(power) + power_units)
        power = 0
        r, g, b = GetColor(power)
    OutputText(energy, power, r, g, b)
    return energy, power, r, g, b

def ShouldRun():
    shining, city, sunrise, sunset, now = SunShining()
    return shining and solarDataJob.should_run

solarDataJob = schedule.every(5).minutes.do(GetSolarData)
pushNotificationJob = schedule.every(1).hours.do(SendPushNotification)

try:
    #prime the pump
    energy = 0
    power = 0
    r = 0
    g = 0
    b = 0
    logger.info("Restart - " + TimeStamp() )
    energy, power, r, g, b = ProcessSolar(True, energy, power, r, g, b)

    while True:
        energy, power, r, g, b = ProcessSolar(ShouldRun(), energy, power, r, g, b)
except Exception as e:
    logger.exception("Solar service crashed. Error: %s", e) 

