#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import time

from lowlevel import LowLevelApi
#from game import GameApi
from point import Point
from constants import *
from mac import Image

## Tests ##
if __name__ == '__main__':
	
	# Drag HP pot to slot 7
	api = LowLevelApi()
	hp = api.loadIcon('assets/hp.png').hash()
	for slot in range(1, 9):
		icon = api.getSlotImage(slot).hash()
		isHp = icon == hp
		print 'Slot {0} HP={1}'.format(slot, isHp)
		if isHp:
			api.dragSlotToSlot(slot, 7)
			break