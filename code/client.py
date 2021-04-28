#!/usr/bin/env python3

import socket, pickle, sys
#from card import Card
from network import TCPNetwork
from deckmanager import DeckManager
from player import Player
import json
import time
#to remove
from deck import Deck

class Client:
	def __init__(self, server_address, server_port):
		self.__server_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__socket_game	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__server_info	= (server_address, server_port)
		self.__game_info	= None
		self.__deckmanager	= DeckManager()
		self.__player 		= None

	def menu(self):
		print("0 - Launch a random match")
		print("1 - Rejoindre une partie (unavailabe for now)")
		print("2 - Démarrer une partie")
		print("3 - Quitter")
		print("4 - Debug ")
		return int(input("Choix : "))

	########################################################################
	############			PROTOTYPES IN UML			####################
	########################################################################

	# communicate with the server via udp
	# sets the game socket and infos
	def connect_server(self,):
		self.__server_socket.settimeout(10.0)
		msg = "Hello Python!"
		address_game = self.__server_info
		while True:
			c = self.menu()
			
			# asks to join a game
			if c == 0:
				msg = "game"
				self.__server_socket.sendto(msg.encode(),self.__server_info)
				try:
					data,addr = self.__server_socket.recvfrom(1024)
					print ("Received Messages:",pickle.loads(data)," from",addr)
					self.__game_info = pickle.loads(data)
				except socket.timeout:
					print('Request timed out')
				break
				
#			# asks for a list of existing games to join
#			if c == 1:
#				msg = "join"
#				self.__server_socket.sendto(msg.encode(),self.__server_info)
#				try:
#					data,addr = self.__server_socket.recvfrom(1024)
#					print ("Received Messages:",pickle.loads(data)," from",addr)
#					self.__game_info = pickle.loads(data)
#				except socket.timeout:
#					print('Request timed out')
#				break
#				
#				
			# asks to create a new game
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
				
			# quit
			elif c == 3:
				break
				
			# connect to a game directly through it's port
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
			
			
			
			card = ("cardname","test","haha")
			self.__socket_game.send(pickle.dumps(card))

			print ('Data Sent to Server')

			rcard = pickle.loads(self.__socket_game.recv(4096))
			
			print('Received', rcard)
			#print('Received', rcard.to_string())

	def send_action():
		pass

	def receive_action():
		pass

	def play():
		pass

	def mulligan(self):
		#counter mulligan
		c = 0
		while c<=7:
			# pioche
			self.__player.draw_card(7-c)
			self.__player.debug_print_hand()
			#choose to mulligan
			m = str(input("mulligan ? y/n"))
			if m=='y' :
				c+=1
				# vider la main
				self.__player.get_board().empty_hand()
				# shuffle deck
				self.__player.get_board().get_deck().shuffle()
			else :
				break
		





	def start_phase():
		pass

	def main_phase():
		pass

	def battle_phase():
		pass

	def end_phase():
		pass

	def test(self):

		deck = None

		self.__deckmanager.add()
		self.__deckmanager.add()

		self.__deckmanager.remove(0)

		deck = self.__deckmanager.get_deck(0)

#		for card in deck.get_cards():
#			print(card.to_string())

		print("BREAKPOINT")
	
		
		self.__player = Player(20,deck)
		
		#self.__player.debug_print_hand()
		#self.mulligan()
		#self.__player.debug_print_hand()
		
		
		self.__player.draw_card(7)
		self.__player.debug_print_hand()
		self.__player.play_card(0)
		print("------------")
		print("|battlezone|")
		print("------------")
		self.__player.debug_print_battle_zone()

		self.__player.to_graveyard("BATTLE_ZONE", 0)

		self.__player.debug_print_battle_zone()

		print("------")
		print("|hand|")
		print("------")
		self.__player.debug_print_hand()


		
########################################################################


def main():

	client = None

#	if len(sys.argv) != 3:
#		print("Usage : %s host_server port_server" % sys.argv[0])
#		print("Où :")
#		print("  host_server : adresse IPv4 du serveur")
#		print("  port_server : numéro de port d'écoute du serveur")
#		sys.exit(-1)


	try:
		with open("ip_config.json") as file:
			json_string = json.load(file)
			host_server = json_string['host_server']
			port_server = int(json_string['port_server'])
	except OSError:
		#sys.exit("Impossible d'ouvrir le fichier JSON")
		print("the ip_config file could not be loaded")
		host_server = str(input("host_server"))
		port_server = int(input("port_server"))


	if port_server < 1024:
		print("Port invalide")
		sys.exit(-1)

	client = Client(host_server, port_server)

	client.test()

	client.connect_server()
	client.connect_game()
	print("YAY")


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)



























