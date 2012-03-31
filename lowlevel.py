#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from point import Point

GAME_TITLE = 'Realm of the Mad God'
GAME_SIZE = Point(800, 600)

print '[d] Platform:', sys.platform
if sys.platform == 'darwin':
	from mac import PlatformSpecificApi
else:
	from linux import PlatformSpecificApi

class LowLevelApi(PlatformSpecificApi):
	def __init__(self):
		self.initGameWindow(GAME_TITLE)
		try:
			self.verticalWindowOffset = self.getVerticalWindowOffset()
		except Exception as error: 
			print '[e]', error