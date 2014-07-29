#!/usr/bin/python

# Copyright 2012, Nathan Milford

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Modified by Stephen Arifin
# July 28th, 2014

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# This script requires:
# * PyUSB 1.0+, apt in Debian/Ubuntu installs 0.4.
# * The ImageTk library. On Debian/Ubuntu 'sudo apt-get install python-imaging-tk'
# Also, unless you want to toggle with udev rules, it needs to be run as root

# Use arrows to aim.  Sse the left enter to fire.

# BTW, Leeroy Jenkins Mode .wav is from: http://www.leeroyjenkins.net/soundbites/warcry.wav

import os
import sys
import time
import pygame
import usb.core
import threading

class launchControl():
   def __init__(self):
      self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
      if self.dev is None:
         raise ValueError('Launcher not found.')
      if self.dev.is_kernel_driver_active(0) is True:
         self.dev.detach_kernel_driver(0)
      self.dev.set_configuration()
      self.lock = threading.Lock()

#      self.master.bind("<KeyPress-Up>", self.turretUp)
#      self.master.bind("<KeyRelease-Up>", self.turretStop)

#      self.master.bind("<KeyPress-Down>", self.turretDown)
#      self.master.bind("<KeyRelease-Down>", self.turretStop)

#      self.master.bind("<KeyPress-Left>", self.turretLeft)
#      self.master.bind("<KeyRelease-Left>", self.turretStop)

#      self.master.bind("<KeyPress-Right>", self.turretRight)
#      self.master.bind("<KeyRelease-Right>", self.turretStop)

#      self.master.bind("<KeyPress-Return>", self.turretFire)










   def turretUp(self):
      self.lock.acquire()
      print "Turret Up."
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) 
      self.lock.release()

   def turretDown(self):
      self.lock.acquire()
      print "Turret Down."
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])
      self.lock.release()

   def turretLeft(self):
      self.lock.acquire()
      print "Turret Left."
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])
      self.lock.release()

   def turretRight(self):
      self.lock.acquire()
      print "Turret Right."
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])
      self.lock.release()

   def turretStop(self):
      self.lock.acquire()
      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])
      self.lock.release()      

   def turretFire(self):
      self.lock.acquire()
      print "FIRE!"

      self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])
      time.sleep(2)
      self.lock.release()
