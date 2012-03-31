#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from Quartz import *
from LaunchServices import * # kUTType constants

from errors import WindowException, NotImplementedException
from point import Point
from constants import *

class Image:
	data = None
	
	def __init__(self, src):
		self.data = src
	
	def isEqual(self, image):
		raise NotImplementedException() #TODO


class PlatformSpecificApi:
	def initGameWindow(self):
		windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
		self.window = None
		for window in windowList:
			if kCGWindowName in window and GAME_TITLE in window[kCGWindowName]:
				self.window = window
				break
		if self.window:
			print '[d]', window
			self.windowId = window[kCGWindowNumber]
		else:
			raise WindowException('Can not find game window')
	
	def loadIcon(self, filename):
		raise NotImplementedException() #TODO
	
	def getSlot(self, point):
		raise NotImplementedException() #TODO
		
	def getVerticalWindowOffset(self):
		return 93 #TODO
	
	def getLocalOffset(self):
		return Point(self.window[kCGWindowBounds]['Width'] / 2 - GAME_SIZE.x / 2, self.verticalWindowOffset)
		
	def getOffset(self):
		bounds = self.window[kCGWindowBounds]
		localOffset = self.getLocalOffset()
		return Point(bounds['X'] + localOffset.x, bounds['Y'] + localOffset.y)
		
	def click(self, point):
		raise NotImplementedException() #TODO
		
	def drag(self, pointA, pointB):
		raise NotImplementedException() #TODO
	
	def sendkey(self, key):
		raise NotImplementedException() #TODO
	
	def testPixel(self, point, colorCode):
		raise NotImplementedException() #TODO
	
	def saveScreenshot(self, filename):
		windowImage = CGWindowListCreateImageFromArray(CGRectNull, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		url = NSURL.fileURLWithPath_(filename)
		imageDestination = CGImageDestinationCreateWithURL(url, kUTTypePNG, 1, None)
		CGImageDestinationAddImage(imageDestination, windowImage, None)
		CGImageDestinationFinalize(imageDestination)