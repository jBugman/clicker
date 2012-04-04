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
				print '[d] Loot {0} is HP: {1}'.format(i, self.game.checkLootItemInSlot(i, ['hp']))
			self.locked = False

class Tests:
	def dragDrop(self):
		# Drag HP pot to slot 7
		api = LowLevelApi()
		api.enterFrame()
		hp = api.loadIcon('assets/hp.png')
		for slot in range(1, 9):
			icon = api.getSlotImage(slot)
			api.saveImage(icon.imageRef, 'test/slot{0}.png'.format(slot))
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
	# tests.dragDrop()
	tests.loot()
