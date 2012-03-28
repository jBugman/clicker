#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import wnck
import sys
from pymouse import PyMouse
import time

SIZE_X = 800
SIZE_Y = 600

HEALTH = (760, 265)
NEXUS = (780, 213)

screen = wnck.screen_get_default()
screen.force_update()

game = None
for win in screen.get_windows():
	title = win.get_name()
	if 'Realm of the Mad God' in title:
		game = (win, gtk.gdk.window_foreign_new(win.get_xid()))
if not game:
	print '[e] Window not found'
	sys.exit(1)

def getPixbuf(win, offset):
	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, SIZE_X, SIZE_Y)
	pb = pb.get_from_drawable(win, win.get_colormap(), offset[2], offset[3], 0, 0, SIZE_X, SIZE_Y)

print '[i] Success'

def getOffset(win):
	geom = game[1].get_geometry()
	origin = game[1].get_origin()
	x = geom[2] / 2 - SIZE_X / 2
	y = 103
	offset = (origin[0] + x, origin[1] + y, x, y)
	return offset

offset = getOffset(game[1])

print '[d] Offset:', offset
game[0].activate(int(time.time()))

mouse = PyMouse()

def click(point):
	old = mouse.position()
	mouse.click(offset[0] + point[0], offset[1] + point[1], 1)
	mouse.move(old[0], old[1])

def testPixel(point, code):
	img = game[1].get_image(offset[2] + point[0], offset[3] + point[1], 1, 1)
	pixel = img.get_pixel(0, 0)
	if not code:
		print pixel
	return pixel == code

while True:
	if testPixel(HEALTH, 5526612): # серый цвет на полоске хп
		print 'PANIC!'
		if testPixel(NEXUS, 460551): # черный цвет на иконке "нексуса" - можем телепортироваться в нексус
			click(NEXUS)
		else:
			print '[d] Already here!'
	time.sleep(0.1)
