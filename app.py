#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from lowlevel import LowLevelApi
#from game import GameApi
from point import Point
from constants import *

## Tests ##
if __name__ == '__main__':
	api = LowLevelApi()
	api.saveImage(api.getWindowScreenshot(), 'test/test.png')
	slot = api.getSlotImage(INVENTORY[0])
	
	from mac import Image
	slot = Image(slot)
	api.saveImage(slot.imageRef, 'test/slot.png')
	slot2 = Image(api.getSlotImage(INVENTORY[1]))
	api.saveImage(slot2.imageRef, 'test/slot2.png')
	tSlot = Image(api.getSlotImage(INVENTORY[0]))
	api.saveImage(tSlot.imageRef, 'test/tSlot.png')
	print '1=2', slot.isEqual(slot2)
	print '1=~1', slot.isEqual(tSlot)
	print '1=1', slot.isEqual(slot)
	print '2=2', slot2.isEqual(Image(api.getSlotImage(INVENTORY[1])))
	
	print 'nexus', api.testPixel(NEXUS, 460551)
	print 'hp', api.testPixel(Point(712, 271), 5526612)
	#print api.getOffset()
	
	#play = Point(410, 555)
	#print play, play + Point(10, 100), play
	
	
	#api.click(play)
	#slotOffset = Point(16, 16)
	#slot1 = Point(618, 412) + slotOffset
	#slot6 = Point(662, 456) + slotOffset
	#api.drag(slot1, slot6)
	#game = GameApi()
