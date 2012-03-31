#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from point import Point

print '[d] Platform:', sys.platform
if sys.platform == 'darwin':
	from mac import PlatformSpecificApi
else:
	from linux import PlatformSpecificApi

class LowLevelApi(PlatformSpecificApi):
	def __init__(self):
		self.initGameWindow()
		try:
			self.verticalWindowOffset = self.getVerticalWindowOffset()
		except Exception as error: 
			print '[e]', error