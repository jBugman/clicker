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
	api = LowLevelApi()
	api.saveImage(api.getWindowScreenshot(), 'test/test.png')

	hp = api.loadIcon('assets/hp.png').hash()
	bow = api.loadIcon('assets/bow1.png').hash()

	t0 = time.time()
	for i, p in enumerate(INVENTORY):
		slot = api.getSlotImage(p)
		api.saveImage(slot.imageRef, 'test/slot{}.png'.format(i + 1))
		#print 'slot{0} hp={1} bow={2}'.format(i + 1, slot.isEqual(hp), slot.isEqual(bow))
		slot = slot.hash()
		print 'slot{0} hp={1} bow={2}'.format(i + 1, slot == hp, slot == bow)
		#slot.isEqual(hp)
		#slot.isEqual(bow)
	print '[d] Taken {:.2f}ms'.format((time.time() - t0) * 1000)
	
	# api.saveImage(slot.imageRef, 'test/slot.png')
	# slot2 = api.getSlotImage(INVENTORY[1])
	# api.saveImage(slot2.imageRef, 'test/slot2.png')
	# tSlot = Image(api.getSlotImage(INVENTORY[0]))
	# api.saveImage(tSlot.imageRef, 'test/tSlot.png')
	# print '1=2', slot.isEqual(slot2)
	# print '1=~1', slot.isEqual(tSlot)
	# print '1=1', slot.isEqual(slot)
	# print '2=2', slot2.isEqual(Image(api.getSlotImage(INVENTORY[1])))
	
	# print 'nexus', api.testPixel(NEXUS, 460551)
	# print 'hp', api.testPixel(Point(712, 271), 5526612)
	 
	# hp = api.loadIcon('assets/hp.png')
	# api.saveImage(hp.imageRef, 'test/thp.png')
	# print '1=hp', slot.isEqual(hp)
	 
	# hp = Image(api.loadIcon('test/slot.png'))
	# print '2=hp', slot2.isEqual(hp)
	# s2 = api.loadIcon('assets/bow1.png')
	# print '1=s2', slot.isEqual(s2)
	# print '2=s2', slot2.isEqual(s2)
	
	# print 'as', Image(api.loadIcon('assets/hp.png')).isEqual(Image(api.loadIcon('assets/hp.png')))
	
	# print api.getOffset()
	
	# play = Point(410, 555)
	# print play, play + Point(10, 100), play
	
	
	# api.click(play)
	# slotOffset = Point(16, 16)
	# slot1 = Point(618, 412) + slotOffset
	# slot6 = Point(662, 456) + slotOffset
	# api.drag(slot1, slot6)
	# game = GameApi()
