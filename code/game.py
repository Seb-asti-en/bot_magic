#!/usr/bin/env python3

#from card import Card
import socket, pickle
#from player import Player
class Game:
	def __init__(self, server_address, server_port, nb_client=2):
		self.__socket	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__info		= (server_address, server_port)
		self.__nb_client= nb_client
		self.__conn 	= None
	def get_socket(self):
		return self.__socket

	def wait_client(self):
		self.__socket.bind(self.__info)
		self.__socket.listen(5)
		self.__conn = [0]*self.__nb_client
		address 	= [0]*self.__nb_client
		i=0
		while i<self.__nb_client:
			self.__conn[i], address[i] = self.__socket.accept()
			print('Connected by', address)
			i+=1

	def start(self):
		while True:
			for i in range(self.__nb_client):
				data = self.__conn[i].recv(4096)
				if not data:
					break
				data_variable = pickle.loads(data)
				print('Data received from client :')
				print(data_variable)
				self.__conn[i].send(data)


