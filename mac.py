#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os, os.path
import time
import hashlib
from Quartz import *
from LaunchServices import * # kUTType constants
from AppKit import NSEvent, NSRunningApplication, NSApplicationActivateIgnoringOtherApps

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
		return self.hash() == image.hash()
		
	def hash(self):
		hashSrc = ''
		for y in range(self.height):
			for x in range(self.width):
				p = Point(x, y)
				hashSrc += str(self.getPixel(p))
		return hashlib.md5(hashSrc).hexdigest()
	
	def getPixel(self, point):
		byteIndex = long(self.BYTES_PER_PIXEL * (self.width * point.y + point.x))
		r = ord(self.data[byteIndex])
		g = ord(self.data[byteIndex + 1])
		b = ord(self.data[byteIndex + 2])
		#a = ord(self.data[byteIndex + 3])
		return r * 256 * 256 + g  * 256 + b


class Mouse:
	@staticmethod
	def press(point):
		event = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, point.asTuple(), 0)
		CGEventPost(kCGHIDEventTap, event)
	
	@staticmethod
	def release(point):
		event = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, point.asTuple(), 0)
		CGEventPost(kCGHIDEventTap, event)
	
	@staticmethod
	def move(point):
		move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, point.asTuple(), 0)
		CGEventPost(kCGHIDEventTap, move)
	
	@staticmethod
	def position():
		loc = NSEvent.mouseLocation()
		return Point(loc.x, CGDisplayPixelsHigh(0) - loc.y)

class Keyboard:
	@staticmethod
	def keydown(keycode):
		event = CGEventCreateKeyboardEvent(None, CG_KEY_CODES[str(keycode)], True)
		CGEventPost(kCGHIDEventTap, event)

	@staticmethod
	def keyup(keycode):
		event = CGEventCreateKeyboardEvent(None, CG_KEY_CODES[str(keycode)], False)
		CGEventPost(kCGHIDEventTap, event)
	
	@staticmethod
	def press(keycode):
		Keyboard.keydown(keycode)
		time.sleep(0.05)
		Keyboard.keyup(keycode)

class PlatformSpecificApi:
	def initGameWindow(self):
		windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
		self.window = None
		for window in windowList:
			if kCGWindowName in window and GAME_TITLE in window[kCGWindowName]:
				self.window = window
				break
		if self.window:
			if 'Firefox' in self.window[kCGWindowOwnerName]:
				raise WindowException('Firefox not supported. Use Google Chrome')
			self.windowId = window[kCGWindowNumber]
		else:
			raise WindowException('Can not find game window')
			
		self.hashes = {}
		for filename in os.listdir('grabbed-images'):
			if filename.endswith('.png'):
				asset = self.loadIcon(os.path.join('grabbed-images', filename))
				if asset:
					h = asset.hash()
					self.hashes[h] = asset
		print '[d] Hashes: ', len(self.hashes)
	
	def loadIcon(self, filename):
		imgDataProvider = CGDataProviderCreateWithCFData(NSData.dataWithContentsOfFile_(filename))
		imageRef = CGImageCreateWithPNGDataProvider(imgDataProvider, None, True, kCGRenderingIntentDefault)
		if imageRef:
			return Image(imageRef)
		else:
			return None
	
	def getImageAtPoint(self, point, size = Point(32, 32)):
		point = point + self.getOffset() + Point(1, 2)
		rect = CGRectMake(point.x, point.y, size.x, size.y)
		imageRef = CGWindowListCreateImageFromArray(rect, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		image = Image(imageRef)
		
		h = image.hash()
		if not h in self.hashes:
			print '[i] Grabbed new asset'
			self.hashes[h] = image
			self.saveImage(image.imageRef, os.path.join('grabbed-images', str(h) + '.png'))
			
		return image
		
	def getVerticalWindowOffset(self):
		MAX_OFFSET = 300 # Возможный отступ
		bounds = self.window[kCGWindowBounds]
		searchRect = CGRectMake(bounds['X'] + bounds['Width'] / 2 - 1, bounds['Y'] + GAME_SIZE.y, 3, MAX_OFFSET)
		searchRectImage = CGWindowListCreateImageFromArray(searchRect, [self.windowId], kCGWindowImageBoundsIgnoreFraming)
		searchRectImage = Image(searchRectImage)
		for y in range(0, MAX_OFFSET):
			if searchRectImage.getPixel(Point(0, y)) == 0x000 and searchRectImage.getPixel(Point(1, y)) == 0x000 and searchRectImage.getPixel(Point(2, y)) == 0x000:
				return y - 2 # Не ясно пока, почему нужна поправка, но пусть будет
		return 0
	
	def getLocalOffset(self):
		return Point(self.window[kCGWindowBounds]['Width'] / 2 - GAME_SIZE.x / 2, self.verticalWindowOffset)
		
	def getOffset(self):
		bounds = self.window[kCGWindowBounds]
		localOffset = self.getLocalOffset()
		return Point(bounds['X'] + localOffset.x, bounds['Y'] + localOffset.y)
	
	def activateWindow(self):
		app = NSRunningApplication.runningApplicationWithProcessIdentifier_(self.window[kCGWindowOwnerPID])
		app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
	
	def click(self, point):
		oldPosition = Mouse.position()
		point = point + self.getOffset()
		time.sleep(0.05)
		self.activateWindow()
		time.sleep(0.05)
		Mouse.press(point)
		Mouse.release(point)
		time.sleep(0.001)
		Mouse.move(oldPosition)
	
	def drag(self, pointA, pointB):
		pointA = pointA + self.getOffset()
		pointB = pointB + self.getOffset()
		oldPosition = Mouse.position()
		time.sleep(0.05)
		self.activateWindow()
		time.sleep(0.05)
		Mouse.press(pointA)
		time.sleep(0.05)
		Mouse.move(pointB)
		time.sleep(0.2)
		Mouse.release(pointB)
		time.sleep(0.2)
		Mouse.move(oldPosition)
	
	def sendkey(self, key):
		self.activateWindow()
		time.sleep(0.05)
		Keyboard.press(key)
	
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

CG_KEY_CODES = {
	'shift': 56,
	'1': 18,
	'2': 19,
	'3': 20,
	'4': 21,
	'5': 23,
	'6': 22,
	'7': 26,
	'8': 28,
	'tilda': 50
}