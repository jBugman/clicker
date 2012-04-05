#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import time
from Quartz import *

class Timer:
	def start(self):
		self.t = time.time()
		
	def get(self):
		return (time.time() - self.t) * 1000
		
	def format(self):
		return '{0:.2f}ms'.format(self.get())

t = Timer()

t.start()
windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
for window in windowList:
	if kCGWindowOwnerName in window and 'Google' in window[kCGWindowOwnerName]:
		break
print '[i] Get window:', t.format()

# t.start()
# windowImage = CGWindowListCreateImageFromArray(CGRectNull, [window[kCGWindowNumber]], kCGWindowImageBoundsIgnoreFraming)
# print '[i] Full image:', t.format()
# 
def cropCGImage(image, cropRect):
	bitsPerComponent = CGImageGetBitsPerComponent(image)
	bytesPerRow = CGImageGetBytesPerRow(image) / CGImageGetWidth(image) * cropRect.size.width
	context = CGBitmapContextCreate(None, cropRect.size.width, cropRect.size.height, bitsPerComponent, bytesPerRow, CGColorSpaceCreateDeviceRGB(), CGImageGetBitmapInfo(image))
	CGContextDrawImage(context, ((-cropRect.origin.x, -cropRect.origin.y), cropRect.size), image)
	return CGBitmapContextCreateImage(context)

# t.start()
# ta = 0
# for i in range (10):
# 	rect = CGRectMake(10 * i, 20, 32, 32)
# 	frame = CGWindowListCreateImageFromArray(rect, [window[kCGWindowNumber]], kCGWindowImageBoundsIgnoreFraming)
# 	t0 = t.get()
# 	ta += t0
# 	print '[i] 32x32 image:', t0
# print '[i] Total: {0}ms'.format(ta)

t.start()
ta = 0
windowImage = CGWindowListCreateImageFromArray(CGRectNull, [window[kCGWindowNumber]], kCGWindowImageBoundsIgnoreFraming)
for i in range (10):
	rect = CGRectMake(10 * i, 20, 32, 32)
	frame = cropCGImage(windowImage, rect)
	t0 = t.get()
	ta += t0
	print '[i] 32x32 cropped image:', t0
print '[i] Total: {0}ms'.format(ta)


# import gtk.gdk
# 
# t.start()
# w = gtk.gdk.get_default_root_window()
# sz = w.get_size()
# print "The size of the window is %d x %d" % sz
# pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
# pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
# if (pb != None):
#     pb.save("screenshot.png","png")
#     print "Screenshot saved to screenshot.png."
# else:
#     print "Unable to get the screenshot."
# print '[i] GTK screenshot:', t.format()

import subprocess
from PIL import Image
 
t.start()
filename = 'test/screencapture.png'
subprocess.call(['screencapture', '-l', str(window[kCGWindowNumber]), filename])
im = Image.open(filename)
im.load()
print '[i] screencapture+pil screenshot:', t.format()

t.start()
ta = 0
for i in range (10):
	rect = (10 * i, 20, 10 * i + 32, 52)
	frame = im.crop(rect)
	frame.load()
	t0 = t.get()
	ta += t0
	print '[i] 32x32 cropped image:', t0
print '[i] Total: {0}ms'.format(ta)


# from AppKit import *
# t.start()
# subprocess.call(['screencapture', '-c', '-l', '2399'])
# pb = NSPasteboard.generalPasteboard()
# pbi = pb.pasteboardItems()[0]
# print 'pasteboard', pbi.types()
# img = NSImage.alloc().initWithPasteboard_(pb)
# tiff = img.TIFFRepresentation()
# bm = NSBitmapImageRep.imageRepWithData_(tiff)
# png = NSBitmapImageRep.representationOfImageRepsInArray_usingType_properties_(img.representations(), NSPNGFileType, None)
#image = Image.fromstring('RGB', tiff)
# print '[i] screencapture+pasteboard screenshot:', t.format()