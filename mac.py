#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from Quartz import *
from LaunchServices import * # kUTType constants

from errors import WindowException, NotImplementedException
from point import Point
from constants import *

class Image:
	data = None
	BYTES_PER_PIXEL = 4
	BITS_PER_COMPONENT = 8
	COLOR_SPACE = CGColorSpaceCreateDeviceRGB()
	
	def __init__(self, src):
		self.imageRef = src
		self.width = CGImageGetWidth(self.imageRef)
		self.height = CGImageGetHeight(self.imageRef)
				
		bytesPerRow = self.BYTES_PER_PIXEL * self.width
		size = bytesPerRow * self.height
		rawData = Foundation.NSMutableData.dataWithLength_(size)
		context = CGBitmapContextCreate(rawData, self.width, self.height, self.BITS_PER_COMPONENT, bytesPerRow, self.COLOR_SPACE, kCGImageAlphaPremultipliedLast | kCGBitmapByteOrder32Big)
		CGContextDrawImage(context, CGRectMake(0, 0, self.width, self.height), self.imageRef)
		
		self.data = rawData
	
	def isEqual(self, image):
		if len(self.data) != len(image.data):
			return False
		for i, byte in enumerate(image.data):
			if byte != self.data[i]:
				return False
		return True
	
	def getPixel(self, point):
		byteIndex = long(self.BYTES_PER_PIXEL * (self.width * point.y + point.x))
		r = ord(self.data[byteIndex])
		g = ord(self.data[byteIndex + 1])
		b = ord(self.data[byteIndex + 2])
		#a = ord(self.data[byteIndex + 3])
		return r * 256 * 256 + g  * 256 + b


class PlatformSpecificApi:
	def initGameWindow(self):
		windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
		self.window = None
		for window in windowList:
			if kCGWindowName in window and GAME_TITLE in window[kCGWindowName]:
				self.window = window
				break
		if self.window:
			self.windowId = window[kCGWindowNumber]
		else:
			raise WindowException('Can not find game window')
	
	def loadIcon(self, filename):
		raise NotImplementedException() #TODO
	
	def getSlotImage(self, point):
		point = point + self.getOffset() + Point(1, 2)
		rect = CGRectMake(point.x, point.y, 32, 32)
		image = CGWindowListCreateImageFromArray(rect, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		return image
		
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
		point = point + self.getOffset()
		rect = CGRectMake(point.x, point.y, 1, 1)
		imageRef = CGWindowListCreateImageFromArray(rect, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		image = Image(imageRef)
		return colorCode == image.getPixel(Point(0, 0))
	
	# Additional test methods
	
	def getWindowScreenshot(self):
		windowImage = CGWindowListCreateImageFromArray(CGRectNull, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		return windowImage
	
	def saveImage(self, image, filename):
		url = NSURL.fileURLWithPath_(filename)
		imageDestination = CGImageDestinationCreateWithURL(url, kUTTypePNG, 1, None)
		CGImageDestinationAddImage(imageDestination, image, None)
		CGImageDestinationFinalize(imageDestination)