#!/usr/bin/env python

# This simple script is run whenever an image has finished loading from the
# mjpeg-streamer and is sent to the ImageListener thread
# 
# Created by Stephen Arifin
# July 28th, 2014 

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 420
BUFFER_SIZE = 1024
MESSAGE = 'ready'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
s.close()

