#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import os, os.path

from lowlevel import LowLevelApi
from point import Point
from constants import *

CHECK_INTERVAL = 0.25 # секунды

COLORS = {
	'NOHP': 5526612, # серый цвет на полоске хп
	'NEXUS_MARKER': 460551 # черный цвет на иконке "нексуса" - можем телепортироваться в нексус
}

# States
UNDEFINED = 'undefined'
CAN_TELEPORT = 'can_teleport'

class GameApi:
	state = UNDEFINED
	icons = None

	lowHpThreshold = 50
	criticalHpThreshold = 30

	def __init__(self):
		self.api = LowLevelApi()
		# Event callbacks
		self.stateChange = self.nope
		self.lowHp = self.nope
		self.criticalHp = self.nope
		self.hasLoot = self.nope
		self.stateChange = self.nope
		# Loading assets
		self.icons = {}
		for filename in os.listdir('assets'):
			if filename.endswith('.png'):
				self.icons[os.path.splitext(filename)[0]] = self.api.loadIcon(os.path.join('assets', filename))
		print '[d] Assets:', len(self.icons)

	def nope(self):
		print '[w] Not implemented'

	def checkState(self):
		if self.api.testPixel(NEXUS, COLORS['NEXUS_MARKER']):
			if self.state != CAN_TELEPORT:
				self.state = CAN_TELEPORT
				self.stateChange(CAN_TELEPORT)
		elif self.state != UNDEFINED:
			self.state = UNDEFINED
			self.stateChange(UNDEFINED)

	def checkHP(self):
		criticalHealth = Point(HEALTH_BASE.x + int(1.0 * self.criticalHpThreshold / 100 * HEALTH_SIZE), HEALTH_BASE.y)
		lowHealth = Point(HEALTH_BASE.x + int(1.0 * self.lowHpThreshold / 100 * HEALTH_SIZE), HEALTH_BASE.y)
		if self.api.testPixel(criticalHealth, COLORS['NOHP']):
			self.criticalHp()
		elif self.api.testPixel(lowHealth, COLORS['NOHP']):
			self.lowHp()

	def checkLoot(self):
		loot8 = self.api.getLootImage(8)
		return loot8.isEqual(self.icons['empty'])

	def checkLootItemInSlot(self, slot, acceptedItems):
		lootSlot = self.api.getLootImage(slot, checkHashes = True)
		for item in acceptedItems:
			if lootSlot.isEqual(self.icons[item]):
				return item
		return None

	def run(self):
		while True:
			self.api.enterFrame()
			self.checkState()
			if self.state == CAN_TELEPORT:
				self.checkHP()
			if self.checkLoot():
				self.hasLoot()
			self.api.exitFrame()
			time.sleep(CHECK_INTERVAL)

#EOF
