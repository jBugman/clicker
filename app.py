#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from lowlevel import LowLevelApi
#from game import Game
#from point import Point

## Tests ##
if __name__ == '__main__':
	api = LowLevelApi()
	api.saveScreenshot('test/test.png')
	#play = Point(410, 555)
	#slotOffset = Point(16, 16)
	#slot1 = Point(618, 412).addOffset(slotOffset)
	#slot6 = Point(662, 456).addOffset(slotOffset)
	#api.drag(slot1, slot6)
	#game = Game()
