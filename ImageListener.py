#!/usr/bin/env python

# This thread is in charge of listening to a folder for image files.
# If an image is produced, it sends a signal to the AutoTurret thread
# saying that the image is done being created and is ready to be analyzed
#
# Created by Stephen Arifin
# July 28th, 2014

import threading
import socket
from AutoTurret import *

class ImageListener(threading.Thread):
	
	# Server information
	TCP_IP = '' # local host
	TCP_PORT = 420 #open port 420 for connection
	BUFFER_SIZE = 1024  

	# If an image is ready
	ready = False

	def __init__(self, launcher):
		threading.Thread.__init__(self)
		self.autoturret = AutoTurret(launcher)
		self.count = 0

	def run(self):
		# Starts the autoturret thread
		self.autoturret.setDaemon(True)
		self.autoturret.start()			


		# Waits for a TCP signal from the mjpeg-streamer
		# to signal when an image is ready
		print 'Image Listener Starting...'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.TCP_IP, self.TCP_PORT))
		s.listen(1)
		conn, addr = s.accept()

		while 1:
    			data = conn.recv(self.BUFFER_SIZE)
    			if not data:
        			s.listen(1)
        			conn, addr = s.accept()
    			if data == 'ready':
				self.count += 1
				if self.count == 2:
					print 'image ready'
					self.autoturret.ready()
					self.count = 0

	def getAuto(self):
		return self.autoturret

	def stop(self):
		self.conn.close()
                self._Thread__stop()
