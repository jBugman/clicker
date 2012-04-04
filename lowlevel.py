#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from point import Point
from constants import INVENTORY, LOOT

print '[d] Platform:', sys.platform
if sys.platform == 'darwin':
	from mac import PlatformSpecificApi
else:
	from linux import PlatformSpecificApi

class LowLevelApi(PlatformSpecificApi):
	def __init__(self):
		self.initGameWindow()
		try:
			self.verticalWindowOffset = self.getVerticalWindowOffset()
		except Exception as error: 
			print '[e]', error
	
	def getSlotImage(self, slotNumber):
		point = INVENTORY[slotNumber - 1]
		return self.getImageAtPoint(point, True)

	def getLootImage(self, slotNumber, checkHashes = False):
		point = LOOT[slotNumber - 1]
		return self.getImageAtPoint(point, checkHashes)

	def dragSlotToSlot(self, slotNumberA, slotNumberB):
		pointA = INVENTORY[slotNumberA - 1] + Point(16, 16)
		pointB = INVENTORY[slotNumberB - 1] + Point(16, 16)
		self.drag(pointA, pointB)

	def dragLootToSlot(self, slotNumberA, slotNumberB):
		pointA = LOOT[slotNumberA - 1] + Point(16, 16)
		pointB = INVENTORY[slotNumberB - 1] + Point(16, 16)
		self.drag(pointA, pointB)