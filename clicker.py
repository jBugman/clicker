#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk, wnck
import sys
from pymouse import PyMouse
import time
import os, os.path

## Local constants
GAME_TITLE = 'Realm of the Mad God'
CHECK_INTERVAL = 0.1 # секунды

CHICKEN_THRESHOLD = 30 # %
POTION_THRESHOLD = 60 # %

## Coords
COORDS = {
	'GAMESCREEN': (800, 600),
	'HEALTH_BASE': (612, 271, 176),
	'NEXUS': (780, 213)
}
INVENTORY = [
	(618, 412),
	(662, 412),
	(706, 412),
	(750, 412),
	(618, 456),
	(662, 456),
	(706, 456),
	(750, 456)
]
LOOT = [
	(618, 512),
	(662, 512),
	(706, 512),
	(750, 512),
	(618, 556),
	(662, 556),
	(706, 556),
	(750, 556)
]
ITEMS = {
	'HP_POT': 'hp_pot',
	'NOTHING': '-'
}

### Colors
COLOR = {
	'NOHP': 5526612, # серый цвет на полоске хп
	'NEXUS_MARKER': 460551, # черный цвет на иконке "нексуса" - можем телепортироваться в нексус
	'BACKGROUND_BLACK': 0 # фон страницы, вне игры
}

class Watcher:
	useChicken = True
	isLooting = False

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
		self.chickenHealth = (COORDS['HEALTH_BASE'][0] + int(1.0 * CHICKEN_THRESHOLD / 100 * COORDS['HEALTH_BASE'][2]), COORDS['HEALTH_BASE'][1])
		self.potionHealth = (COORDS['HEALTH_BASE'][0] + int(1.0 * POTION_THRESHOLD / 100 * COORDS['HEALTH_BASE'][2]), COORDS['HEALTH_BASE'][1])

		self.assets = {
			'hp': self.loadImage('hp'),
			'slot1': self.loadImage('slot1'),
			'slot2': self.loadImage('slot2'),
			'slot3': self.loadImage('slot3'),
			'slot4': self.loadImage('slot4'),
			'slot5': self.loadImage('slot5'),
			'slot6': self.loadImage('slot6'),
			'slot7': self.loadImage('slot7'),
			'slot8': self.loadImage('slot8'),
			'empty': self.loadImage('empty'),
		}
		self.updateInventory()
		self.printInventory()

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

	def drag(self, pointA, pointB):
		oldCoords = self.mouse.position()
		offset = self.getOffset()
		self.mouse.press(offset[0] + pointA[0], offset[1] + pointA[1], 1)
		self.mouse.move(offset[0] + pointB[0], offset[1] + pointB[1])
		time.sleep(0.05)
		self.mouse.release(offset[0] + pointB[0], offset[1] + pointB[1], 1)
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
			if self.testPixel(COORDS['NEXUS'], COLOR['NEXUS_MARKER']): # проверяем, что мы в игре (не в нексусе, точнее)
				if self.testPixel(self.chickenHealth, COLOR['NOHP']):
					print '[!] Chicken!'
					self.click(COORDS['NEXUS'])

				elif self.testPixel(self.potionHealth, COLOR['NOHP']):
					print '[i] HP needed'
					self.updateInventory()
					if len(self.hpPotions):
						slot = self.hpPotions[-1]
						print '[i] Drinking Hp potion in slot {0}'.format(slot)
						os.system('xvkbd -text {0}'.format(slot))
					else:
						print '[w] No HP potions=('

			if not self.isLooting and self.checkLoot():
				print '[d] Loot!'
				slots = self.getLootSlot()
				if slots:
					self.isLooting = True
					pointA = (LOOT[slots[0] - 1][0] + 16, LOOT[slots[0] - 1][1] + 16)
					pointB = (INVENTORY[slots[1] - 1][0] + 16, INVENTORY[slots[1] - 1][1] + 16)
					self.drag(pointA, pointB)
					self.isLooting = False

			time.sleep(CHECK_INTERVAL)

	def loadImage(self, name):
		pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('assets', name + '.png'))
		pixmap = gtk.gdk.Pixmap(self.game, 32, 32, -1)
		pixmap.draw_pixbuf(None, pixbuf, 0, 0, 0, 0, -1, -1)
		return pixmap.get_image(0, 0, 32, 32)

	def updateInventory(self):
		offset = self.getOffset()
		i = 1
		result = []
		hpPots = []
		emptySlots = []
		for coords in INVENTORY:
			slot = self.game.get_image(offset[2] + coords[0] + 1, offset[3] + coords[1], 32, 32)
			if self.compareImages(slot, self.assets['hp']):
				result.append(ITEMS['HP_POT'])
				hpPots.append(i)
			elif self.compareImages(slot, self.assets['slot1']) or \
					 self.compareImages(slot, self.assets['slot2']) or \
					 self.compareImages(slot, self.assets['slot3']) or \
	 		 		 self.compareImages(slot, self.assets['slot4']) or \
					 self.compareImages(slot, self.assets['slot5']) or \
			 		 self.compareImages(slot, self.assets['slot6']) or \
	 		 		 self.compareImages(slot, self.assets['slot7']) or \
	 		 		 self.compareImages(slot, self.assets['slot8']):
				result.append(ITEMS['NOTHING'])
				emptySlots.append(i)
			else:
				result.append('?')
			i += 1
		self.inventory = result
		self.hpPotions = hpPots
		self.emptySlots = emptySlots

	def checkLoot(self):
		offset = self.getOffset()
		slot = self.game.get_image(offset[2] + LOOT[7][0] + 1, offset[3] + LOOT[7][1], 32, 32)
		return self.compareImages(slot, self.assets['empty'])

	def getLootSlot(self):
		offset = self.getOffset()
		i = 1
		for coords in LOOT:
			slot = self.game.get_image(offset[2] + coords[0] + 1, offset[3] + coords[1], 32, 32)
			if self.isItemGood(slot):
				self.updateInventory()
				if not len(self.emptySlots):
					print '[w] Inventory is full!'
					return None
				else:
					inventorySlot = self.emptySlots[-1]
					print '[d] Looting item from loot slot {0} to inventory slot {1}'.format(i, inventorySlot)
					return (i, inventorySlot)
		i += 1

	def isItemGood(self, item):
		return True

	def printInventory(self):
		i = 1
		for item in self.inventory:
			print 'Slot {0}: {1}'.format(i, item)
			i += 1

	def compareImages(self, imageA, imageB, size = (32, 32)):
		for x in range(0, size[0] - 1):
			for y in range(0, size[1] - 1):
				if imageA.get_pixel(x, y) != imageB.get_pixel(x, y):
					return False
		return True

watcher = Watcher(True)
print '[i] Watching..'
watcher.runLoop()

# EOF
