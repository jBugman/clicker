#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import os, os.path

from lowlevel import LowLevelApi
from point import Point
from constants import *

CHECK_INTERVAL = 0.1 # секунды

COLORS = {
	'NOHP': 5526612, # серый цвет на полоске хп
	'NEXUS_MARKER': 460551 # черный цвет на иконке "нексуса" - можем телепортироваться в нексус
}

# States
UNDEFINED = 'undefined'
CAN_TELEPORT = 'can_teleport'
HP_OK = 'ok'
HP_LOW = 'low_hp'
HP_CRITICAL = 'critical_hp'

class GameApi:
	state = UNDEFINED
	hp = HP_OK
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
		for fileName in os.listdir('assets'):
			self.icons[os.path.splitext(fileName)[0]] = self.api.loadIcon(os.path.join('assets', fileName))

	def nope(self):
		print '[w] Not implemented'

	def checkState(self):
		if self.api.testPixel(NEXUS, COLOR['NEXUS_MARKER']):
			if self.state != CAN_TELEPORT:
				self.state = CAN_TELEPORT
				self.stateChange(CAN_TELEPORT)
			else:
				self.state = UNDEFINED
				self.stateChange(UNDEFINED)

	def checkHP(self):
		criticalHealth = Point(HEALTH_BASE.x + int(1.0 * self.criticalHpThreshold / 100 * HEALTH_SIZE), HEALTH_BASE.y)
		lowHealth = Point(HEALTH_BASE.x + int(1.0 * self.lowHpThreshold / 100 * HEALTH_SIZE), HEALTH_BASE.y)
		if self.testPixel(criticalHealth, COLORS['NOHP']):
			if self.hp != HP_OK or self.hp != HP_LOW:
				self.hp = HP_CRITICAL
				self.criticalHp()
#			elif self.hp != HP_OK or self.hp != HP_CRITICAL:
#				self.hp = HP_LOW
#				self.lowHp()
#			else:
#				self.hp = HP_OK

	def run(self):
		while True:
			self.checkState()
			if self.state == CAN_TELEPORT:
				self.checkHP()
			time.sleep(CHECK_INTERVAL)

#EOF
