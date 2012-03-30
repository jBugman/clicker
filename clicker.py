#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import sys
from pymouse import PyMouse
import time
import os, os.path

from winapi import Api

## Local constants


CHICKEN_THRESHOLD = 30 # %
POTION_THRESHOLD = 60 # %

## Coords


ITEMS = {
	'HP_POT': 'hp_pot',
	'NOTHING': '-'
}

### Color

class Watcher:
	isLooting = False

	def __init__(self):

		self.api = Api()
		self.game = self.api.getGtkWindow()

		self.chickenHealth = (COORDS['HEALTH_BASE'][0] + int(1.0 * CHICKEN_THRESHOLD / 100 * COORDS['HEALTH_BASE'][2]), COORDS['HEALTH_BASE'][1])
		self.potionHealth = (COORDS['HEALTH_BASE'][0] + int(1.0 * POTION_THRESHOLD / 100 * COORDS['HEALTH_BASE'][2]), COORDS['HEALTH_BASE'][1])

		self.updateInventory()
		self.printInventory()

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


watcher = Watcher(True)
print '[i] Watching..'
watcher.runLoop()

# EOF
