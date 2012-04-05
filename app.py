#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import time, sys

from lowlevel import LowLevelApi
from game import GameApi
from point import Point
from constants import *

class Clicker:
	def __init__(self):
		self.locked = False

		self.game = GameApi()
		self.game.lowHp = self.lowHp
		#self.game.criticalHp =
		self.game.stateChange = self.stateChange
		self.game.hasLoot = self.hasLoot

		self.acceptedLoot = self.lootBetterThanTier(1)
		self.acceptedLoot.append('hp')
		print '[d] Accepted loot:', self.acceptedLoot

	def start(self):
		try:
			self.game.run()
		except KeyboardInterrupt:
			print '[i] Exiting..'
			sys.exit(0)

	def lowHp(self):
		print '[i] Low HP' # FIXME: not working?

	def stateChange(self, state):
		print '[i] State:', state

	def hasLoot(self):
		if not self.locked:
			print '[i] Loot!'
			self.locked = True
			for i in range(1, 8):
				item = self.game.checkLootItemInSlot(i, self.acceptedLoot)
				if item:
					print '[d] Loot:', item
					self.game.api.dragLootToSlot(i, 8)
			self.locked = False

	def lootBetterThanTier(self, tier):
		result = []
		for key in self.game.icons.keys():
			if not key.startswith('slot') and key[-1].isdigit() and int(key[-1]) >= tier:
				result.append(key)
		return result

class Tests:
	def dragDrop(self):
		# Drag HP pot to slot 7
		api = LowLevelApi()
		api.enterFrame()
		hp = api.loadIcon('assets/hp.png')
		for slot in range(1, 9):
			icon = api.getSlotImage(slot)
			#api.saveImage(icon.imageRef, 'test/slot{0}.png'.format(slot))
			isHp = icon.isEqual(hp)
			print 'Slot {0} HP={1}'.format(slot, isHp)
			if isHp:
				api.dragSlotToSlot(slot, 7)
				break
		api.exitFrame()

	def loot(self):
		# Check HP pots in loot
		Clicker().start()

if __name__ == '__main__':
	tests = Tests()
	#tests.dragDrop()
	tests.loot()
