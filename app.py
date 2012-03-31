#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from lowlevel import LowLevelApi
#from game import GameApi
from point import Point

## Tests ##
if __name__ == '__main__':
	api = LowLevelApi()
	api.saveScreenshot('test/test.png')
	play = Point(410, 555)
	print play, play + Point(10, 100), play
	print api.getOffset()
	#api.click(play)
	#slotOffset = Point(16, 16)
	#slot1 = Point(618, 412) + slotOffset
	#slot6 = Point(662, 456) + slotOffset
	#api.drag(slot1, slot6)
	#game = GameApi()
