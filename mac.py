#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from Quartz import *
from LaunchServices import * # kUTType constants

from errors import WindowException, NotImplementedException
from point import Point

class Image:
	data = None
	
	def __init__(self, src):
		self.data = src
	
	def isEqual(self, image):
		raise NotImplementedException() #TODO


class PlatformSpecificApi:
	def initGameWindow(self, title):
		windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
		self.window = None
		for window in windowList:
			if kCGWindowName in window and title in window[kCGWindowName]:
				self.window = window
				break
		if self.window:
			self.windowId = window[kCGWindowNumber]
		else:
			raise WindowException('Can not find game window')
	
	def loadIcon(self, filename):
		raise NotImplementedException() #TODO
	
	def getSlot(self, point):
		raise NotImplementedException() #TODO
		
	def getVerticalWindowOffset(self):
		raise NotImplementedException() #TODO
	
	def getLocalOffset(self):
		raise NotImplementedException() #TODO
		
	def getOffset(self):
		raise NotImplementedException() #TODO
		
	def click(self, point):
		raise NotImplementedException() #TODO
		
	def drag(self, pointA, pointB):
		raise NotImplementedException() #TODO
	
	def sendkey(self, key):
		raise NotImplementedException() #TODO
	
	def testPixel(self, point, colorCode):
		raise NotImplementedException() #TODO
	
	def saveScreenshot(self, filename):
		windowImage = CGWindowListCreateImage(CGRectNull, kCGWindowListOptionIncludingWindow, self.windowId, kCGWindowImageBoundsIgnoreFraming)
		url = NSURL.fileURLWithPath_(filename)
		imageDestination = CGImageDestinationCreateWithURL(url, kUTTypePNG, 1, None)
		CGImageDestinationAddImage(imageDestination, windowImage, None)
		CGImageDestinationFinalize(imageDestination)