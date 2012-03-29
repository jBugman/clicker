#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import webkit
import threading

class Game(gtk.Window):
	def __init__(self):
		super(Game, self).__init__()
		self.connect('destroy', self.destroy)
		self.set_title('Realm of the Mad God :: Automated')
		self.set_size_request(800, 600)
		self.set_resizable(False)
		browser = webkit.WebView()
		self.add(browser)
		self.set_icon_from_file('assets/hp.png')
		self.show_all()
		browser.open('http://realmofthemadgod.com')
		self.browser = browser

	def run(self):
		gtk.main()

	def destroy(self, widget, data = None):
		if self.runloop and self.runloop.isAlive():
			self.runloop._Thread__stop()
		gtk.main_quit()

#thread = threading.Thread(target = test_loop, args = ())
#thread.start()

game = Game()
#game.runloop = thread
game.run()
