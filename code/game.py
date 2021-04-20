#!/usr/bin/env python3

from card import Card
import socket
#from player import Player
class Game:
	def __init__(self, server_address, server_port):
		self.__socket	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__info		= (server_address, server_port)

	def get_socket(self):
		return self.__socket

	def wait_client(self):
		self.__socket.bind(self.__info)
		self.__socket.listen(5)
		nb_client =2
		conn 	= [0]*nb_client
		address = [0]*nb_client
		i=0
		while i<nb_client:
			i+=1
			conn[i], address[i] = self.__socket.accept()
			print('Connected by', address)

	def start(self):
		while True:
			data = game.get_socket().recv(4096)
			if not data:
				break
			data_variable = pickle.loads(data)
			print('Data received from client :')
			print(data_variable)
			game.get_socket().send(data)


