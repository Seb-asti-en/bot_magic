#!/usr/bin/env python3

import socket, pickle
from player import Player
from deckmanager import DeckManager

SOCKET = 0
PLAYER = 1
LIFE = 20
SEGMENT_SIZE = 65536

class Game:

	def __init__(self, socket, slots = 2):
		self.__socket = socket
		self.__deckmanager = DeckManager()
		self.__slots = slots
		self.__players = []

	def get_socket(self):
		return self.__socket
	
	def netconfig(self):
		return self.__socket.getsockname()

	def is_full(self):
		return len(self.__players) >=  self.__slots

	def wait_client(self):

		# Mise en écoute de la socket TCP
		self.__socket.listen(self.__slots)

		# Connexions des joueurs
		while not self.is_full():
			self.__players.append([self.__socket.accept()[0],None])

	def choose_deck(self):

		deck = None

		for player in self.__players:

			# Création automatique du deck sans demander au client
			self.__deckmanager.add()
			deck = self.__deckmanager.copy_deck(0)

			# Création de l'objet Player en lui passant le deck
			player[PLAYER] = Player(LIFE,deck)

	def mulligan(self, index):

		mulligan_count = 0
		user_input = ""

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		while mulligan_count <= 7:

			# Pioche (7-n) cartes
			self.__players[index][PLAYER].draw_card(7 - mulligan_count)

			self.__players[index][PLAYER].debug_print_hand()

			# Demande à l'utilisateur
			user_input = input("Voulez-vous mulligan ? (oui/non) \n>")
			
			# Traitement de l'entrée
			if user_input == "oui":

				# Défausse de la main
				self.__players[index][PLAYER].get_board().empty_hand()
				
				# Mélange du deck
				self.__players[index][PLAYER].get_board().get_deck().shuffle()

				mulligan_count += 1
			
			else:
				break

	def start(self):

		raw_data = None
		data = None

		# # Debug : Affichage des cartes du deck
		# for card in self.__players[0][PLAYER].get_board().get_deck().get_cards():
		# 	print(card.to_string())
		
		# input("Appuyez sur la touche Entrée")

		# self.__players[0][PLAYER].debug_print_hand()
		# self.mulligan(0)
		# self.__players[0][PLAYER].debug_print_hand()

		while True:

			for player in self.__players:
				
				# Réception depuis le client : Deck (TCP)(1)
				raw_data = player[SOCKET].recv(SEGMENT_SIZE)
				
				if not raw_data:
					break
				
				data = pickle.loads(raw_data)

				print('Données recues :', data.get_cards()[0].to_string())

				# Envoi vers le client : Deck (TCP)(2)
				player[SOCKET].send(raw_data)

			break

