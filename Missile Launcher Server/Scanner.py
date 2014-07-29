#!/usr/bin/env python

# This thread is in charge of scanning the room if the autoturret thread
# does not find any faces after a certain period of time. It is also
# in charge of firing automatically when the autoturret thread is
# locked on to a target.
#
# Created by Stephen Arifin
# July 28th, 2014


import threading
import random
import time
from LaunchControl import *

class Scanner(threading.Thread):
	
	# These values show the amount of images past until
	# the turret goes to either fire mode or scanning
	# mode
	FIRE_LIMIT = 2
	IDLE_LIMIT = 7

	def __init__(self, launcher):
		threading.Thread.__init__(self)
		self.launcher = launcher	
		self.fireCount = 0
		self.idleCount = 0
		self.targets = False

		# The boundary variable allows the turret to 
		# change the probability it goes left or right
		# based off of its previous actions
		self.boundary = 3
		self.scannerStatus = False

	def run(self):
		while(1):
			if self.scannerStatus:

				# If the target has been locked on for two
				# images, the turret will fire
				if self.fireCount >= self.FIRE_LIMIT and self.targets:
					self.launcher.turretFire()
					
					# Reset the fire count
					self.fireCount = 0

				# If the autoturret does not see a face
				# for over 7 images, it will start scanning
				# the room for potential victims
				if self.idleCount >= self.IDLE_LIMIT and not self.targets:
					self.randomMovement()
					self.idleCount = 2

	# Randomly choose a direction and how long to turn			
	def randomMovement(self):
		#randomly choose a direction
		direction = random.randint(0, 7)
		
		# turn left
		if 0 <= direction < self.boundary:
			self.launcher.turretLeft()
			turnTime = random.uniform(.5, 1.25)
			time.sleep(turnTime)
			self.launcher.turretStop()
			if self.boundary > 0:
				self.boundary -= 1

		# turn right
		elif self.boundary <= direction <= 5:
			self.launcher.turretRight()
			turnTime = random.uniform(.5, 1.25)
			time.sleep(turnTime)
			self.launcher.turretStop()
			if self.boundary < 5:
				self.boundary += 1

		# turn up for what
		elif direction == 6:
			self.launcher.turretUp()
			turnTime = random.uniform(.1, .25)
			time.sleep(turnTime)
			self.launcher.turretStop()

		# turn down for what
		elif direction == 7:
			self.launcher.turretUp()
			turnTime = random.uniform(.1, .25)
			time.sleep(turnTime)
			self.launcher.turretStop()

	
	def updateFireCount(self):
		self.fireCount += 2
		self.idleCount = 0

	def updateIdleCount(self):
		if self.fireCount > 0:
			self.fireCount -= 1
                self.idleCount += 1

	def foundFaces(self):
		self.idleCount = 0
		self.targets = True;

	def noFaces(self):
		self.targets = False

	def updateScannerStatus(self, state):
		self.scannerStatus = state
