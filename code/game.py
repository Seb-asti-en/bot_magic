#!/usr/bin/env python3

from card import Card
#from player import Player
class Game:
	def __init__(self, server_address, server_port):
		self.__socket	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__info		= (server_address, server_port)




	def start(self):
#		self.__socket.bind((host_server, port_server))
#		self.__socket.listen(5)
#		conn, address = self.__socket.accept()
#		conn.close()
#		self.__socket.close()
	
		pass

c = Card("hello", 3)
print (c.get_name())
