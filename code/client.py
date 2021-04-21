#!/usr/bin/env python3

import socket, pickle, sys
from card import Card
from network import TCPNetwork

class Client:
	def __init__(self, server_address, server_port, deck_manager):
		self.__server_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__socket_game	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__server_info	= (server_address, server_port)
		self.__game_info	= None
		self.__deck_manager	= deck_manager


	def menu(self):
		print("1 - Rejoindre une partie")
		print("2 - Démarrer une partie")
		print("3 - Quitter")
		return int(input("Choix : "))




	########################################################################
	############			PROTOTYPES IN UML			####################
	########################################################################

	# communicate with the server via udp
	# either asks to create a new game or for a list of existing ones to join
	def connect_server(self,):
		self.__server_socket.settimeout(10.0)
		msg = "Hello Python!"
		address_game = self.__server_info
		while True:
			c = self.menu()
			if c == 1:
				msg = "join"
				self.__server_socket.sendto(msg.encode(),self.__server_info)
				try:
					data,addr = self.__server_socket.recvfrom(1024)
					print ("Received Messages:",pickle.loads(data)," from",addr)
					self.__game_info = pickle.loads(data)
				except socket.timeout:
					print('Request timed out')
				break
				
				
			elif c == 2:
				msg = "ng"
				self.__server_socket.sendto(msg.encode(),self.__server_info)
				try:
					data,addr = self.__server_socket.recvfrom(1024)
					print ("Received Messages:",pickle.loads(data)," from",addr)
					self.__game_info = pickle.loads(data)
				except socket.timeout:
					print('Request timed out')
				break
				print(self.__game_info)
			elif c == 3:
				break
			elif c == 4:
				print ("this is intended for debugging")
				a = str(input("adress"))
				b = int(input("port"))
				self.__game_info = (a, b)
				print(self.__game_info)
				break
			else :
				pass

	# connect to the chosen game
	def connect_game(self):
		if self.__game_info != None:
			print(self.__game_info)
			self.__socket_game.connect(self.__game_info)
			
			card = Card("","","cardname","","",
			[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],"","","")
			self.__socket_game.send(pickle.dumps(card))

			print ('Data Sent to Server')

			rcard = pickle.loads(self.__socket_game.recv(4096))
			
			print('Received', rcard)
			print('Received', rcard.to_string())

	def send_action():
		pass

	def receive_action():
		pass

	def play():
		pass

	def start_phase():
		pass

	def main_phase():
		pass

	def battle_phase():
		pass

	def end_phase():
		pass

########################################################################


def main():
	if len(sys.argv) != 3:
		print("Usage : %s host_server port_server" % sys.argv[0])
		print("Où :")
		print("  host_server : adresse IPv4 du serveur")
		print("  port_server : numéro de port d'écoute du serveur")
		sys.exit(-1)

	host_server = str(sys.argv[1])
	port_server = int(sys.argv[2])

	if port_server < 1024:
		print("Port invalide")
		sys.exit(-1)

	client = Client(host_server, port_server, None)
	client.connect_server()
	client.connect_game()
	print("YAY")
	#connect_game(adress_game)

#	network = TCPNetwork(host_server, port_server)
#	network.connect(host_server, port_server)
#	
#	loop = True

#	while loop:
#		while True:
#			choix = menu()
#			if choix >= 1 and choix <= 3:
#				break
#		loop = contact_server(network, choix)




if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)



























