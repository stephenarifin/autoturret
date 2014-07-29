#!/usr/bin/env python

# This module contains the face detection algorithm and adjusts
# the turret to lock on to the target
#
# Created by Stephen Arifin
# July 28th, 2014

import os
import cv2
import cv2.cv as cv
import numpy as np
import time
import threading
from LaunchControl import *
from ImageListener import * 
from Scanner import *

# The location of the face cascade for face detection
FACE_CASCADE_PATH = './opencv/OpenCV-2.4.3/data/haarcascades/haarcascade_frontalface_default.xml'

# The location of the source images from the webcam to be processed
IMG_INPUT_PATH = './mjpg-streamer/mjpg-streamer/pics/'

# The constants that relate the distance the target away is
# and the time needed for the turret to turn
SMALL_DELAY_CONSTANT = .0034
LARGE_DELAY_CONSTANT = .0032

# The error allowed for adjustments
HORIZONTAL_ERROR = 20
VERTICAL_ERROR = 40

class AutoTurret(threading.Thread):

	def __init__(self, launcher):
		threading.Thread.__init__(self)
		self.face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
		self.turretOn = False
		self.launcher = launcher
		self.trackingOn = False
		self.imageReady = threading.Event()
		self.scanner = Scanner(launcher)
		self.img = None
		self.outline = None
#		self.count = 0


	# Processes an image and returns a list of rectangles 
	# of all the faces detected in the image
	# (Returns an empty list if no faces are detected)

	def detectFaces(self, img):
		
		# Grayscales the image for faster/more accurate face detection
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Equalizes the image for more accurate results
		gray = cv2.equalizeHist(gray)

		# Processes an image and returns a list of rectangles
		# with the coordinates of all the faces
		#
		# Uses the fastest ScaleFactor, the bare minimum of neighbors,
		# and a large minimum face size to maximize processing speed
		# for the Beaglebone. Also uses to Canny Pruning to increase
		# efficiency of face detection
		outlines = self.face_cascade.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=2, minSize=(50, 50), flags = cv.CV_HAAR_DO_CANNY_PRUNING)
		
		# If there is no face detected, update the scanner count
		# and return an empty list
		if len(outlines) == 0:
			self.scanner.noFaces()
			self.scanner.updateIdleCount()
			return []

		# If faces are found, update the scanner and return
		# the list of rectangles
		print 'Faces Found'
		self.scanner.foundFaces()
		outlines[:,2:] += outlines[:,:2]
		return outlines


	# Draws a rectangle on the image and saves the file
	# in a folder. Used mainly for debugging

#	def drawRect(self, img, outline):
#		if not len(outlines) == 0:
#		x1, y1, x2, y2 = outline
#		cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0) ,2)
#		cv2.circle(img, ((x1 + x2)/2, (y1 + y2)/2), 10, (0, 0, 255), -1)
#		cv2.imwrite('./test/detected' +  str(self.count) + '.jpg', img)
#		self.count += 1
	
	# Gets a rectangle of the target and adjusts the launcher to aim
	# at the center of the target. The amount of time the launcher turns
	# is based off of the distance multiplied by a specific constant

	def tracking(self, img, target):

		# Gets the x and y coords. of the center of the screen
		centerHeight, centerWidth, depth = img.shape
		centerX = centerWidth / 2
		centerY = centerHeight / 2

		# Gets the x and y coords. of the center of the target
		x1, y1, x2, y2 = target
		targetX = (x1 + x2) / 2
		targetY = (y1 + y2) / 2

		# Adjusts the launcher based off the distance away
		# from the target
		if targetX > (centerX + HORIZONTAL_ERROR):
			self.launcher.turretRight()
			time.sleep(self.calculateHorizontalDelay(centerX, targetX))
			self.launcher.turretStop()
		elif targetX < (centerX - HORIZONTAL_ERROR):
                        self.launcher.turretLeft()
                        time.sleep(self.calculateHorizontalDelay(centerX, targetX))
                        self.launcher.turretStop()
		elif targetY < (centerY - VERTICAL_ERROR):
                        self.launcher.turretUp()
                        time.sleep(self.calculateVerticalDelay(centerY, targetY))
                        self.launcher.turretStop()
			self.scanner.updateFireCount()
		elif targetY > (centerY + VERTICAL_ERROR):
                        self.launcher.turretDown()
                        time.sleep(self.calculateVerticalDelay(centerY, targetY))
                        self.launcher.turretStop()
			self.scanner.updateFireCount()
		else:
			print 'Locked on'
			self.scanner.updateFireCount()
	
	# Calculates the time needed to turn horizontally
	def calculateHorizontalDelay(self, center, target):
		distance = abs(center - target)
		if distance < 100:
			return SMALL_DELAY_CONSTANT * distance
		else:
			return LARGE_DELAY_CONSTANT * distance
	
	# Calculates the time needed to adjust vertically
	def calculateVerticalDelay(self, center, target):
		return SMALL_DELAY_CONSTANT * abs(center - target)



	# When an image is ready, the autoturret will analyze the image
	# and detect faces in the image. If there are faces detected,
	# the launcher will adjust in order to be on target for the face

	def run(self):

		# Starts the scanner thread
		self.scanner.setDaemon(True)
		self.scanner.start()

		while(1):
			if self.turretOn:
				
				# Waits for an image to be ready from the 
				# ImageListener thread
				self.imageReady.clear()
				print 'autoturret waiting'
				self.imageReady.wait()

				# Reads the second image from the triple
				# buffer and analyzes it
				print 'Detecting...'
				if not (os.listdir(IMG_INPUT_PATH) == []):
					pictures = os.listdir(IMG_INPUT_PATH)
					pictures.sort()
					target = IMG_INPUT_PATH + pictures[len(pictures) - 1]
					print target
					self.img = cv2.imread(target)
					outlines = self.detectFaces(self.img)

					# If faces were found in the image
					if not len(outlines) == 0:
						self.outline = outlines[0]
#						self.drawRect(self.img, self.outline)
						
						# Adjust the launcher
						self.tracking(self.img, self.outline)

				# If no image files were found in the folder
				else:
					print 'no files found'

	def turretStatus(self, state):
		self.turretOn = state
	
	def getScanner(self):
		return self.scanner
	
	def stop(self):
		self.cap.release()
		self._Thread__stop()

	def ready(self):
		self.imageReady.set()
