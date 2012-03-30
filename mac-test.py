#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from Quartz import *
from LaunchServices import * # kUTType* constants

GAME_TITLE = 'Realm of the Mad God'

def getWindow():
	windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
	for window in windowList:
		if kCGWindowName in window and GAME_TITLE in window[kCGWindowName]:
			return window
	return None
	
def saveScreenshot(windowId):
	windowImage = CGWindowListCreateImage(CGRectNull, kCGWindowListOptionIncludingWindow, windowId, kCGWindowImageBoundsIgnoreFraming)
	url = NSURL.fileURLWithPath_('test.png')
	imageDestination = CGImageDestinationCreateWithURL(url, kUTTypePNG, 1, None)
	CGImageDestinationAddImage(imageDestination, windowImage, None)
	CGImageDestinationFinalize(imageDestination)

if __name__ == '__main__':
	window = getWindow()
	saveScreenshot(window[kCGWindowNumber])