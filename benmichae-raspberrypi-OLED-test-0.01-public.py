#!/usr/bin/python
# -*- coding: utf-8 -*-

# benmichae-raspberrypi-OLED-test
# (no c) 2016 @benmichae <benmichae@gmail.com>
#
# Python script for displaying test data on a breakout OLED Screen
# Requires rm-hull/ssd1306 installed on Raspberry PI.
#
# References
# 1. https://github.com/rakshasa/rtorrent/wiki/RPC-Setup-XMLRPC
# 2. https://github.com/mdevaev/emonoda/wiki/rTorrent-XMLRPC-Reference
# 3. https://gist.github.com/query/899683
# 4. https://github.com/rm-hull/ssd1306

import os
import sys
import time
import xmlrpclib # Import XMLRPC library
from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont

scriptname = 'benmichae-raspberrypi-OLED-test'
scriptversion = 'v0.01-20160522-Peschiera Del Garda'

#Yes, Color is my day-long obsession, joy and torment. 
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))

def hostname():
    return "benmichae"

def stats(oled):
    with canvas(oled) as draw:
        font = ImageFont.truetype('fonts/FreeMonoBold.ttf', 20)
        draw.text((0, 0), "benmichae", font=font, fill=255)
        font = ImageFont.truetype('fonts/FreeMono.ttf', 16)   
        draw.text((0, 18), "rpi oled", font=font, fill=255)
        draw.text((0, 30), "i2c test", font=font, fill=255)
        draw.text((0, 42), "more text!", font=font, fill=255)
 
def main():
    oled = ssd1306(port=1, address=0x3C)
    stats(oled)
    prGreen(scriptname) ; prGreen(scriptversion) ; prYellow("Sending Frame of Test Data to SSD1306 OLED over i2C")

if __name__ == "__main__":
    main()