#!/usr/bin/python

# benmichae-rtorrent-datadumpintoterminal
# (no c) 2016 @benmichae <benmichae@gmail.com>
#
# Python library for displaying rtorrent data on a breakout OLED Screen
# Requires rtorrent instatlled, and XML RPC Socket setup. This script is not error tolerant.
#
# References
# 1. https://github.com/rakshasa/rtorrent/wiki/RPC-Setup-XMLRPC
# 2. https://github.com/mdevaev/emonoda/wiki/rTorrent-XMLRPC-Reference
# 3. https://gist.github.com/query/899683
#

scriptname = 'benmichae-rtorrent-get-data-over-xmlrpc'
scriptversion = 'v0.03-20160521-Stavanger'
scriptPrintSeeding = 0
scriptPrintAvailableMethods = 0
scriptPrintAvailableViews = 1

# Import XMLRPC library
import xmlrpclib

#Yes, Color is my day-long obsession, joy and torment. 
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))

#Print Intro Text
prGreen(scriptname)
prYellow(scriptversion)

# Create an object to represent our server. (designed to be ran from device running rtorrent over apache2)
server_url = "http://localhost/rutorrent/plugins/httprpc/action.php";
server = xmlrpclib.Server(server_url);

#Print Server Details
print ''
prRed('Server Details')
hostname = server.system.hostname()	; print ' Hostname        :', hostname
ver = server.system.client_version(); print ' rtorrent ver    :', ver
totalUpload = server.get_up_total()     ; print ' Total Upload    :', totalUpload/1024/1024/1024,'GB'
totalDownload = server.get_down_total() ; print ' Total Download  :', totalDownload/1024/1024/1024,'GB'

#This prints all available system commands (note, verbose ca 1000 lines)
if (scriptPrintAvailableMethods==1) :
 listOfMethods = server.system.listMethods() ; print 'Available Methods' , listOfMethods #lists available methods

#Prints List of Available Views
if (scriptPrintAvailableViews==1) :
 listOfViews = server.view_list(); print ' Available Views: ' , listOfViews #lists available views

#Print Current Speeds
print ''
prRed('Current Speeds')
currentUploadRate = server.get_up_rate() ; print ' Current Upload Rate  :', currentUploadRate/1024,'KB/s'
currentDownloadRate = server.get_down_rate() ; print ' Current Download Rate:', currentDownloadRate/1024,'KB/s'

#Print List of Torrents Currently Leeching
view = server.download_list("", "leeching") # Get torrents in 'leeching' view
print ''
prRed('Torrents Currently Leeching')
# For each torrent in the view
for torrent in view:
    # Print the name of torrent
    print ' -', server.d.get_name(torrent), server.d.get_bytes_done(torrent)/1024/1024, '/', server.d.get_size_bytes(torrent)/1024/1024,'MB ', server.d.get_down_rate(torrent)/1024,'KB/s'

print ''

#Print List of Torrents Currently Seeding (note, verbose, one line for each torrent in system. I prefer this disabled)
if (scriptPrintSeeding==1):
 view = server.download_list("", "seeding") # Get torrents in 'leeching' view
 print ''
 prRed('Torrents Currently Seeding')
 # For each torrent in the view
 for torrent in view:
    # Print the name of torrent
    print ' -', server.d.get_name(torrent), server.d.get_size_bytes(torrent)/1024/1024,'MB'
 print ''

prGreen('---')
