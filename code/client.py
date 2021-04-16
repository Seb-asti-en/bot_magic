#!/usr/bin/env python3

import socket, pickle, sys
from card import Card
from network import Network

def main():
	if len(sys.argv) != 3:
		print("Usage : %s hostServer portServer" % sys.argv[0])
		print("Où :")
		print("  hostServer : adresse IPv4 du serveur")
		print("  portServer : numéro de port d'écoute du serveur")
		sys.exit(-1)

	hostServer = str(sys.argv[1])
	
	portServer = int(sys.argv[2])

	if portServer < 1024:
		print("Port invalide")
		sys.exit(-1)

	loop = True

	while loop:
		while True:
			print("1 - Rejoindre une partie")
			print("2 - Démarrer une partie")
			print("3 - Quitter")
			choix = int(input("Choix : "))
			if choix >= 1 and choix <= 3:
				break

		if choix == 1:
			pass # joinGame()
		if choix == 2:
			pass # createGame()
		if choix == 3:
			loop = False
	
	network = Network(hostServer, portServer)
	network.connect()

	card = Card("","","cardname","","",[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],"","","")
	network.send(card)

	print ('Data Sent to Server')

	data = network.recv(4096)
	rcard = pickle.loads(data)
	print('Received', rcard)
	print('Received', rcard.to_string())

if __name__ == "__main__":
	main()
