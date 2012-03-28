#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import wnck
import sys
from pymouse import PyMouse
import time

## Local constants

BROWSER_OFFSET = 103
CHICKEN_THRESHOLD = 50 # %

## Coords

GAMESCREEN = (800, 600)
HEALTH_BASE = (612, 271, 176)
NEXUS = (780, 213)

### Colors

NOHP_COLOR = 5526612 # серый цвет на полоске хп
NEXUS_MARKER = 460551 # черный цвет на иконке "нексуса" - можем телепортироваться в нексус

screen = wnck.screen_get_default()
screen.force_update()

game = None
for win in screen.get_windows():
	title = win.get_name()
	if 'Realm of the Mad God' in title:
		game = (win, gtk.gdk.window_foreign_new(win.get_xid()))
if not game:
	print '[e] Game window not found'
	sys.exit(1)

print '[i] Watching..'

#def getPixbuf(win, offset):
#	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, SIZE_X, SIZE_Y)
#	pb = pb.get_from_drawable(win, win.get_colormap(), offset[2], offset[3], 0, 0, SIZE_X, SIZE_Y)

def getOffset(win):
	geom = game[1].get_geometry()
	origin = game[1].get_origin()
	x = geom[2] / 2 - GAMESCREEN[0] / 2
	y = BROWSER_OFFSET
	offset = (origin[0] + x, origin[1] + y, x, y)
	return offset

game[0].activate(int(time.time()))

mouse = PyMouse()

def click(point):
	old = mouse.position()
	offset = getOffset(game[1])
	mouse.click(offset[0] + point[0], offset[1] + point[1], 1)
	mouse.move(old[0], old[1])

def testPixel(point, code):
	offset = getOffset(game[1])
	img = game[1].get_image(offset[2] + point[0], offset[3] + point[1], 1, 1)
	pixel = img.get_pixel(0, 0)
	if not code:
		print pixel
	return pixel == code

HEALTH = (HEALTH_BASE[0] + int(1.0 * CHICKEN_THRESHOLD / 100 * HEALTH_BASE[2]), HEALTH_BASE[1])

while True:
	time.sleep(0.05)
	if testPixel(HEALTH, NOHP_COLOR):
		if testPixel(NEXUS, NEXUS_MARKER):
			print '[!] Chicken!'
			click(NEXUS)
