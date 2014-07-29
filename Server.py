#!/usr/bin/env python 

# The Server thread is the main thread that handles all the commands
# sent from the Android phone and controls the launcher in manual mode. 
#
# Created by Stephen Arifin
# July 28th, 2014

import socket
import subprocess
import threading
from LaunchControl import *
from ImageListener import *
from AutoTurret import *


TCP_IP = '' # local host
TCP_PORT = 5005 #open port 5005 for connection
BUFFER_SIZE = 1024  

launcher = launchControl()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print 'Server starting...'

# Creates and starts the ImageListener thread
imagelistener = ImageListener(launcher)
imagelistener.setDaemon(True)
imagelistener.start()

conn, addr = s.accept()

while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        s.listen(1)
        conn, addr = s.accept()
    if data == 'connected\n':
  	print 'Client connected.'
	if not imagelistener.getAuto().turretOn:
		
		# Launches the webcam
 		subprocess.Popen(['./launch_webcam.sh'], shell=True)    
    elif data == 'disconnected\n':
	if not imagelistener.getAuto().turretOn:

		# Kills the webcam
 		subprocess.Popen(['./kill_webcam.sh'], shell=True)
	print 'Client disconnected.'
    elif data == 'up\n':
        launcher.turretUp()
    elif data == 'down\n':
        launcher.turretDown()
    elif data == 'left\n':
        launcher.turretLeft()
    elif data == 'right\n':
        launcher.turretRight()
    elif data == 'fire\n':
        launcher.turretFire()
    elif data == 'stop\n':
         launcher.turretStop()
    elif data == 'auto on\n':
	 print 'autoturret on'
	 imagelistener.getAuto().turretStatus(True)
    elif data == 'auto off\n':
	 print 'autoturret off'
	 imagelistener.getAuto().turretStatus(False)
    elif data == 'scan on\n':
	 print 'scanner on'
	 imagelistener.getAuto().getScanner().updateScannerStatus(True)
    elif data == 'scan off\n':	 
	 print 'scanner off'
	 imagelistener.getAuto().getScanner().updateScannerStatus(False)
conn.close()
