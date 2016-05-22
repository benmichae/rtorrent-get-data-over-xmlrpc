#!/usr/bin/python
# -*- coding: utf-8 -*-

# benmichae-rtorrent-get-data-over-xmlrpc-and-output-onto-raspberrypi-OLED
# (no c) 2016 @benmichae <benmichae@gmail.com>
#
# Python library for displaying rtorrent data on a breakout OLED Screen
# Requires rtorrent installed, XML RPC Socket setup, i2C Enabled on Raspberry PI. This script is not error tolerant.
#
# References
# 1. https://github.com/rakshasa/rtorrent/wiki/RPC-Setup-XMLRPC
# 2. https://github.com/mdevaev/emonoda/wiki/rTorrent-XMLRPC-Reference
# 3. https://gist.github.com/query/899683
# 4. https://github.com/rm-hull/ssd1306
#
# TODO: Scroll active torrent name (or cycle through multiple)

import os
import sys
import time
import xmlrpclib # Import XMLRPC library

from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont

scriptname = 'benmichae-rtorrent-get-data-over-xmlrpc-and-output-onto-raspberrypi-OLED'
scriptversion = 'v0.01-20160521-Peschiera Del Garda'
server_url = "http://localhost/rutorrent/plugins/httprpc/action.php";
debug = 0
server = xmlrpclib.Server(server_url); # Create an object to represent our server. (designed to be ran from device running rtorrent over apache2)
hostnamePI = server.system.hostname();   
truncatehostnameChars = 5 #optionally shorten your hostname (useful for FQDN to Subdomain). 0=no truncate

#Yes, Color is my day-long obsession, joy and torment. 
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))

def getServerULRate(): #GET Server Data
    currentUploadRate = server.get_up_rate()/1024; 
    return currentUploadRate

def getServerDLRate(): #GET Server Data
    currentDownloadRate = server.get_down_rate()/1024;
    return currentDownloadRate

def getLeechingData():
    view = server.download_list("", "leeching") # Get torrents in 'leeching' view
    torrentNameLast = "" 
    for torrent in view:
        torrentNameLast = server.d.get_name(torrent)
        if debug==1:
            print ' -', server.d.get_name(torrent), server.d.get_bytes_done(torrent)/1024/1024, '/', server.d.get_size_bytes(torrent)/1024/1024,'MB ', server.d.get_down_rate(torrent)/1024,'KB/s'
    return torrentNameLast

def hostname():
    if truncatehostnameChars > 0:
        return hostnamePI[:truncatehostnameChars] 
    else:
        return hostnamePI

def rate_ul():
    currentUploadRate = getServerULRate()
    return "U: {:5.0f}".format(currentUploadRate) + " KB/s"

def rate_dl():
    currentDownloadRate = getServerDLRate()
    return "D: {:5.0f}".format(currentDownloadRate) + " KB/s"    

def dlname():
    return torrentNameLast

def stats(oled):
    with canvas(oled) as draw:
        font = ImageFont.truetype('fonts/FreeMonoBold.ttf', 20)
        draw.text((0, 0), hostname(), font=font, fill=255)
        font = ImageFont.truetype('fonts/FreeMono.ttf', 16)   
        draw.text((0, 18), rate_ul(), font=font, fill=255)
        draw.text((0, 30), rate_dl(), font=font, fill=255)
        draw.text((0, 50), getLeechingData(), font=font, fill=255)
 
def main():
    if debug == 1: 
        prGreen(scriptname) ; prGreen(scriptversion)
        prRed('Server Details')
        print ' Hostname        :', hostnamePI   
        ver = server.system.client_version();     
        print ' rtorrent ver    :', ver
        totalUpload = server.get_up_total(); 
        totalDownload = server.get_down_total(); 
        print ' Total Upload    :', totalUpload/1024/1024/1024,'GB'
        print ' Total Download  :', totalDownload/1024/1024/1024,'GB'; print '' 
        prRed('Current Speeds')
        print ' Current Upload Rate  :', rate_ul(),'KB/s'
        print ' Current Download Rate:', rate_dl(),'KB/s'; print '' 
        prRed('Torrents Currently Leeching')
        getLeechingData()
        print ''

    getLeechingData()
    oled = ssd1306(port=1, address=0x3C)
    prGreen(scriptname) ; prGreen(scriptversion) ; prYellow("Sending Data to SSD1306 OLED over i2C -enable debug mode for more info")
    while 1 > 0: #infiniteloop :) probably not best practice. may be revised.            
        stats(oled)
        time.sleep(1)

if __name__ == "__main__":
    main()