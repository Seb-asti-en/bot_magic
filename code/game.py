import socket, pickle, sys, os
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

	def clear_terminal(self):

		command = "clear"

		if os.name == "nt":
			command = "cls"

		os.system(command)

	def wait_client(self):

		# Mise en écoute de la socket TCP
		self.__socket.listen(self.__slots)

		# Connexions des joueurs
		while not self.is_full():
			self.__players.append([self.__socket.accept()[0],None])

	def choose_deck(self):

		player_id = 0
		deck = None

		for player in self.__players:

			# Création automatique du deck sans demander au client
			self.__deckmanager.add()
			deck = self.__deckmanager.copy_deck(0)

			# Création de l'objet Player en lui passant le deck
			player[PLAYER] = Player(player_id,LIFE,deck)
			print(sys.getsizeof(pickle.dumps(player[PLAYER])))

			# Incrémentation du compteur définissant l'identifiant du joueur
			player_id += 1

	def start(self):

		data = None
		serialized_data = None

		# Initialisation de la partie
		for player in self.__players:

			# Sérialisation
			serialized_data = pickle.dumps(player[PLAYER])

			# Envoi vers le player : Objet Player (1)
			player[SOCKET].send(serialized_data)

		# Phase Mulligan
		for player in self.__players:

			# Réponse
			data = "PHASE_START"

			# Rafraichissement de l'écran
			self.clear_terminal()			

			# Sérialisation
			serialized_data = pickle.dumps(data)

			# Envoi vers le player : Démarrage de la phase (2)
			player[SOCKET].send(serialized_data)
		
			# Exécution de la phase
			self.mulligan(player[PLAYER].get_id())

	def mulligan(self, index):

		mulligan_count = 0
		data = None
		serialized_data = None
		response = ""

		# Mélange initial du deck
		self.__players[index][PLAYER].get_board().get_deck().shuffle()

		# Pioche 7 cartes
		self.__players[index][PLAYER].draw_card(7)

		while mulligan_count <= 7:

			# DEBUG
			self.__players[index][PLAYER].debug_print_hand()

			# Réception depuis le client : Requête d'action (3)
			serialized_data = self.__players[index][SOCKET].recv(SEGMENT_SIZE)

			# Désérialisation
			data = pickle.loads(serialized_data)

			# Continuer à mulligan ?
			if(data.get("type") == "MULLIGAN"):

				# Réponse
				response = "ACCEPT"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Acceptation (4)
				self.__players[index][SOCKET].send(serialized_data)

				# Défausse de la main
				self.__players[index][PLAYER].get_board().empty_hand()
				
				# Mélange du deck
				self.__players[index][PLAYER].get_board().get_deck().shuffle()

				# Sérialisation 
				# TODO : (à modifier plus tard selon le format JSON)
				serialized_data = pickle.dumps(self.__players[index][PLAYER])

				# Envoi vers le client : Etat de la partie (5)
				self.__players[index][SOCKET].send(serialized_data)

				mulligan_count += 1

				# Pioche (7-n) cartes
				self.__players[index][PLAYER].draw_card(7 - mulligan_count)
			
			elif(data.get("type") == "SKIP_PHASE"):

				# Réponse
				response = "ACCEPT"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Acceptation (4)
				self.__players[index][SOCKET].send(serialized_data)

				# Sérialisation 
				# TODO : (à modifier plus tard selon le format JSON)
				serialized_data = pickle.dumps(self.__players[index][PLAYER])

				# Envoi vers le client : Etat de la partie (5)
				self.__players[index][SOCKET].send(serialized_data)

				break

			else:

				# Réponse
				response = "DECLINE"

				# Sérialisation
				serialized_data = pickle.dumps(response)

				# Envoi vers le client : Refus (4)
				self.__players[index][SOCKET].send(serialized_data)

				continue 
