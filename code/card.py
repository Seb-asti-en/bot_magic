#!/usr/bin/env python3

class Card:
	def __init__(self, name, cost):
		self._name = name
		self._cost = cost
		
	def get_name(self):
		return self._name

