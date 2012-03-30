#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import gtk
from point import Point

GAME_TITLE = 'Realm of the Mad God'
GAME_SIZE = Point(800, 600)


class ApiException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)



class Image:
	data = None

	def __init__(self, src):
		self.data = src

	def isEqual(self, image):
		for x in range(0, size[0] - 1):
			for y in range(0, size[1] - 1):
				if self.data.get_pixel(x, y) != image.get_pixel(x, y):
					return False
		return True



class Api:
	def __init__(self):
		try:
			self.windowId = subprocess.check_output(['xdotool', 'search', '--name', GAME_TITLE]).strip()
		except subprocess.CalledProcessError:
			raise ApiException('Can not find game window')
		if not self.windowId:
			raise ApiException('Can not find game window')
		self.window = gtk.gdk.window_foreign_new(int(self.windowId))
		if not self.window:
			raise ApiException('Can not get GTK window')
		self.browserOffset = self.getBrowserOffset()

	def loadIcon(self, filename):
		pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		pixmap = gtk.gdk.Pixmap(self.window, 32, 32, -1)
		pixmap.draw_pixbuf(None, pixbuf, 0, 0, 0, 0, -1, -1)
		return Image(pixmap.get_image(0, 0, 32, 32))

	def getSlot(self, point):
		point = point.clone().addOffset(self.getLocalOffset())
		img = self.window.get_image(point.x + 1, point.y, 32, 32)
		return Image(img)

	def getBrowserOffset(self):
		x = self.window.get_geometry()[2] / 2
		for y in range(0, 200):
			img = self.window.get_image(x, y + GAME_SIZE.y, 1, 3)
			if(img.get_pixel(0, 0) == 0x000 and img.get_pixel(0, 1) == 0x000 and img.get_pixel(0, 2) == 0x000):
				return y
		return 0

	def getLocalOffset(self):
		return Point(self.window.get_geometry()[2] / 2 - GAME_SIZE.x / 2, self.browserOffset)

	def getOffset(self):
		origin = self.window.get_origin()
		localOffset = self.getLocalOffset()
		return Point(origin[0] + localOffset.x, origin[1] + localOffset.y)

	def click(self, point):
		point = point.clone().addOffset(self.getOffset())
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId,
										 'mousemove', '--sync', str(point.x), str(point.y),
										 'click', '1',
										 'mousemove', 'restore'])

	def sendkey(self, key):
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId, 'key', key])

	def drag(self, pointA, pointB):
		offset = self.getOffset()
		pointA = pointA.clone().addOffset(offset)
		pointB = pointB.clone().addOffset(offset)
		subprocess.call(['xdotool', 'windowactivate', '--sync', self.windowId,
										 'mousemove', '--sync', str(pointA.x), str(pointA.y),
										 'mousedown', '1',
										 'mousemove', '--sync', str(pointB.x), str(pointB.y),
										 'mouseup', '1',
										 'mousemove', 'restore'])

	def testPixel(self, point, colorCode):
		point = point.clone().addOffset(self.getOffset())
		pixel = self.window.get_image(point.x, point.y, 1, 1).get_pixel(0, 0)
		return pixel == colorCode
