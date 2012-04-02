#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import gtk

from errors import WindowException
from point import Point
from constants import *

class Image:
	data = None

	def __init__(self, src):
		self.data = src

	def isEqual(self, image, size = (32, 32)):
		for x in range(0, size[0] - 1):
			for y in range(0, size[1] - 1):
				if self.data.get_pixel(x, y) != image.data.get_pixel(x, y):
					return False
		return True

class PlatformSpecificApi:
	def initGameWindow(self):
		try:
			self.windowId = subprocess.check_output(['xdotool', 'search', '--name', GAME_TITLE]).strip()
		except subprocess.CalledProcessError:
			raise WindowException('Can not find game window')
		self.window = gtk.gdk.window_foreign_new(int(self.windowId))
		if not self.window:
			raise WindowException('Can not get GTK window')

	def loadIcon(self, filename):
		pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		pixmap = gtk.gdk.Pixmap(self.window, 32, 32, -1)
		pixmap.draw_pixbuf(None, pixbuf, 0, 0, 0, 0, -1, -1)
		return Image(pixmap.get_image(0, 0, 32, 32))

	def getImageAtPoint(self, point, size = Point(32, 32)):
		point = point + self.getLocalOffset()
		img = self.window.get_image(point.x + 1, point.y, size.x, size.y)
		return Image(img)

	def getVerticalWindowOffset(self):
		x = self.window.get_geometry()[2] / 2
		for y in range(0, 200):
			img = self.window.get_image(x, y + GAME_SIZE.y, 1, 3)
			if(img.get_pixel(0, 0) == 0x000 and img.get_pixel(0, 1) == 0x000 and img.get_pixel(0, 2) == 0x000):
				return y
		return 0

	def getLocalOffset(self):
		return Point(self.window.get_geometry()[2] / 2 - GAME_SIZE.x / 2, self.verticalWindowOffset)

	def getOffset(self):
		origin = self.window.get_origin()
		localOffset = self.getLocalOffset()
		return Point(origin[0] + localOffset.x, origin[1] + localOffset.y)

	def click(self, point):
		point = point + self.getLocalOffset()
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId,
										 'mousemove', '--sync', str(point.x), str(point.y),
										 'click', '1',
										 'mousemove', 'restore'])

	def drag(self, pointA, pointB):
		offset = self.getOffset()
		pointA = pointA + offset
		pointB = pointB + offset
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId,
										 'mousemove', '--sync', str(pointA.x), str(pointA.y),
										 'mousedown', '1',
										 'mousemove', '--sync', str(pointB.x), str(pointB.y),
										 'mouseup', '1',
										 'mousemove', 'restore'])

	def testPixel(self, point, colorCode):
		point = point + self.getLocalOffset()
		pixel = self.window.get_image(point.x, point.y, 1, 1).get_pixel(0, 0)
		return pixel == colorCode

	def sendkey(self, key):
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId, 'key', key])
