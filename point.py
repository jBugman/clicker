#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import copy

class Point:
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return '({0}, {1})'.format(self.x, self.y)

	def addOffset(self, offset):
		self.x += offset.x
		self.y += offset.y
		return self

	def clone(self):
		return copy.copy(self)
