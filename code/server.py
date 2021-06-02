#!/usr/bin/env python3
import socket, pickle, sys, json, os
from threading import Thread
from game import Game

PACKET_SIZE = 1024

def main():

	server = None

	server = Server()
	server.run()

class Server:

	def __init__(self):

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__gamelist	= []

		try:
			with open("JSON/ip_config.json") as file:
				json_string = json.load(file)
		except Exception:
			sys.exit("Impossible d'ouvrir le fichier JSON")

		# Nommage de la socket UDP
		self.__socket.bind((json_string['host_server'], int(json_string['port_server'])))

	def run(self):

		request = ""
		client_netconfig = None
		game_netconfig = None
		available_games = []

		while True:

			# Attente de connexion d'un client
			print("En attente de clients...")

			# Réception depuis le serveur : requête initiale (1)
			request,client_netconfig = self.__socket.recvfrom(PACKET_SIZE)

			# print(f"Message reçu : {request} de {client_netconfig[0]}:{client_netconfig[1]}")

			# Traitement de l'information reçue

			# Demande de rejoindre une partie
			if request.decode() == "JOIN_GAME":

				# Vérification de la disponibilité des serveurs
				available_games.clear()
				for game in self.__gamelist:
					if not game.is_full():
						available_games.append(game)

				# Si au moins un serveur de jeu est ouvert
				if len(available_games) > 0:

					print(f"Le client {client_netconfig[0]}:{client_netconfig[1]} rejoint la partie")

					# Envoi vers le serveur : réponse (2)
					self.__socket.sendto(pickle.dumps(("ACCEPT",available_games[0].netconfig())),client_netconfig)

				# Le cas échéant, refus
				else:

					# Envoi vers le serveur : réponse (2)
					self.__socket.sendto(pickle.dumps(("DECLINE","Pas de partie disponible")),client_netconfig)

					print(f"Le client {client_netconfig[0]}:{client_netconfig[1]} tente de rejoindre une partie, mais aucune n'est disponible")

			# Demande de création d'une partie
			elif request.decode() == "NEW_GAME":

				print(f"Le client {client_netconfig[0]}:{client_netconfig[1]} crée une nouvelle partie")

				game_netconfig = self.create_game()

				# Envoi vers le serveur : réponse (2)
				self.__socket.sendto(pickle.dumps(("ACCEPT",game_netconfig)),client_netconfig)

			else:

				print(f"Le client {client_netconfig[0]}:{client_netconfig[1]} a émis une requête invalide")

				# Envoi vers le serveur : réponse (2)
				self.__socket.sendto(pickle.dumps(("DECLINE","Requête invalide")),client_netconfig)

	def create_game(self):

		tcp_socket = None
		game_thread = None

		# Création de la socket pour le serveur de jeu
		tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_socket.bind(('', 0))

		# Création de l'objet Game à passer au thread du serveur de jeu
		game = Game(tcp_socket)

		# Création du thread
		print("Création du thread de la partie")
		game_thread = Thread(target = self.game_thread, args = (game,))

		# Lancement du thread
		game_thread.start()

		# Ajout du serveur de jeu à la liste de parties
		self.__gamelist.append(game)

		return game.netconfig()

	def game_thread(self, game):

		print(f"Lancement de la partie {game.get_socket().getsockname()[1]}")

		game.wait_client()

		game.choose_deck()

		game.start()

		game.turn()

		print("Fermeture du serveur de jeu")

		sys.exit()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		sys.exit(0)
