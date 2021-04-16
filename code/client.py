#!/usr/bin/env python3

import socket, pickle, sys
from card import Card
from network import Network


def menu():
	print("1 - Rejoindre une partie")
	print("2 - Démarrer une partie")
	print("3 - Quitter")
	return int(input("Choix : "))

def contact_server(network, choix):
	#"1 - Rejoindre une partie"
	if choix == 1:
		#send a request
		
		
		card = Card("","","cardname","","",
		[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],"","","")
		network.send(card)

		print ('Data Sent to Server')

		rcard = network.recv(4096)
		
		print('Received', rcard)
		print('Received', rcard.to_string())
		
		
		
		loop = False
	#"2 - Démarrer une partie"
	elif choix == 2:
		#send a request
		loop = False
	#"3 - Quitter"
	elif choix == 3:
		#send a request
		loop = False
	else:
		loop = True
	
	
	
	
	return loop

def join_game():
	pass

def create_game():
	pass

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

	network = Network(hostServer, portServer)
	network.connect()
	
	loop = True

	while loop:
		while True:
			choix = menu()
			if choix >= 1 and choix <= 3:
				break
		loop = contact_server(network, choix)




if __name__ == "__main__":
	main()
