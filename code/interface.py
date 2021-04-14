#!/usr/bin/env python3

class Menu:
	def __init__(self, size):
		self.size = size


class Board:
	def __init__(self):
		self._hand		= []
		self._adv_hand	= []
		self._field		= []
		self._adv_field	= []
	
	def get_hand(self):
		return self._hand
