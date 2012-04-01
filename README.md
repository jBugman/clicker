# Restrictions

1. Not supporting Firefox at all. Really tested only with Chrome.
2. On Mac mouse events are lag-dependent, so there is slight delay in them.
3. Mac version needs it’s own assets (need to be tested if they work with Linux).
4. Image recognition is relatively slow (at least on Mac). Optimization may be needed.
5. Game window activation activates whole application on Mac, so real game window must be on top of it’s window stack.

# Dependencies

## Linux

### xdotool
1. http://semicomplete.googlecode.com/files/xdotool-2.20110530.1.tar.gz
2. [sudo] make all install

### pygtk
1. http://citylan.dl.sourceforge.net/project/macpkg/PyGTK/2.24.0/PyGTK.pkg

## Mac OS X

None (using pure Quartz)