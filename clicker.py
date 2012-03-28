#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import wnck
import sys
from pymouse import PyMouse
import time

## Local constants
GAME_TITLE = 'Realm of the Mad God'
CHECK_INTERVAL = 0.05 # секунды

CHICKEN_THRESHOLD = 50 # %

## Coords
COORDS = {
	'GAMESCREEN': (800, 600),
	'HEALTH_BASE': (612, 271, 176),
	'NEXUS': (780, 213)
}

### Colors
COLOR = {
	'NOHP': 5526612, # серый цвет на полоске хп
	'NEXUS_MARKER': 460551, # черный цвет на иконке "нексуса" - можем телепортироваться в нексус
	'BACKGROUND_BLACK': 0 # фон страницы, вне игры
}

class Watcher:
	useChicken = True

	def __init__(self, useChicken):
		self.useChicken = useChicken

		screen = wnck.screen_get_default()
		screen.force_update()
		for win in screen.get_windows():
			if GAME_TITLE in win.get_name():
				self.game = gtk.gdk.window_foreign_new(win.get_xid())
				break
		if not self.game:
			print '[e] Game window not found'
			sys.exit(1)
		win.activate(int(time.time())) # показываем окно игры

		self.browserOffset = self.getBrowserTopOffset()
		self.mouse = PyMouse()
		self.health = (COORDS['HEALTH_BASE'][0] + int(1.0 * CHICKEN_THRESHOLD / 100 * COORDS['HEALTH_BASE'][2]), COORDS['HEALTH_BASE'][1])

	def getOffset(self):
		origin = self.game.get_origin()
		x = self.game.get_geometry()[2] / 2 - COORDS['GAMESCREEN'][0] / 2
		y = self.browserOffset
		return (origin[0] + x, origin[1] + y, x, y)

	def click(self, point):
		oldCoords = self.mouse.position()
		offset = self.getOffset()
		self.mouse.click(offset[0] + point[0], offset[1] + point[1], 1)
		self.mouse.move(oldCoords[0], oldCoords[1])

	def testPixel(self, point, colorCode):
		offset = self.getOffset()
		pixel = self.game.get_image(offset[2] + point[0], offset[3] + point[1], 1, 1).get_pixel(0, 0)
		return pixel == colorCode

	def getBrowserTopOffset(self):
		x = self.game.get_geometry()[2] / 2
		for y in range(0, 200):
			img = self.game.get_image(x, y + COORDS['GAMESCREEN'][1], 1, 3)
			if (img.get_pixel(0, 0) == COLOR['BACKGROUND_BLACK'] and \
					img.get_pixel(0, 1) == COLOR['BACKGROUND_BLACK'] and \
					img.get_pixel(0, 2) == COLOR['BACKGROUND_BLACK']):
				return y
		sys.exit(2)

	def runLoop(self):
		while True:
			if self.testPixel(COORDS['NEXUS'], COLOR['NEXUS_MARKER']):
				if self.testPixel(self.health, COLOR['NOHP']):
					print '[!] Chicken!'
					self.click(COORDS['NEXUS'])
			time.sleep(CHECK_INTERVAL)

watcher = Watcher(True)
print '[i] Watching..'
watcher.runLoop()

# EOF
