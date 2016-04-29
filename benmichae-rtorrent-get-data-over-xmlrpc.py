#!/usr/bin/python

# benmichae-rtorrent-datadumpintoterminal
# (no c) 2016 @benmichae <benmichae@gmail.com>
#
# Python library for displaying rtorrent data on a breakout OLED Screen
#
# References
# 1. https://github.com/mdevaev/emonoda/wiki/rTorrent-XMLRPC-Reference
# 2. https://gist.github.com/query/899683
#

scriptname = 'benmichae-rtorrent-get-data-over-xmlrpc'
scriptversion = 'v0.01-20160429-Stavanger'

# Import the XMLRPC library
import xmlrpclib

#Yes, Color is my day-long obsession, joy and torment. 
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))

#Intro
prGreen(scriptname)
prYellow(scriptversion)

# Create an object to represent our server. (designed to be ran from device running rtorrent over apache2)
server_url = "http://localhost/rutorrent/plugins/httprpc/action.php";
server = xmlrpclib.Server(server_url);

print ''

prRed('Server Details')
hostname = server.system.hostname()	; print ' Hostname        :', hostname
ver = server.system.client_version(); print ' rtorrent ver    :', ver

totalUpload = server.get_up_total()     ; print ' Total Upload    :', totalUpload/1024/1024/1024,'GB'
totalDownload = server.get_down_total() ; print ' Total Download  :', totalDownload/1024/1024/1024,'GB'

#listOfMethods = server.system.listMethods() ; print 'Available Methods' , listOfMethods #lists available methods
listOfViews = server.view_list(); print ' Available Views: ',
print listOfViews #lists available views

print ''

prRed('Current Speeds')
currentUploadRate = server.get_up_rate() ; print ' Current Upload Rate  :', currentUploadRate/1024,'KB/s'
currentDownloadRate = server.get_down_rate() ; print ' Current Download Rate:', currentDownloadRate/1024,'KB/s'

print ''
# Get torrents in view
view = server.download_list("", "leeching")

prRed('Torrents Currently Leeching')
# For each torrent in the view
for torrent in view:

    # Print the name of torrent
    print ' -', server.d.get_name(torrent), server.d.get_bytes_done(torrent)/1024/1024, '/', server.d.get_size_bytes(torrent)/1024/1024,'MB ', server.d.get_down_rate(torrent)/1024,' KB/sec'

print ''
prGreen('---')
