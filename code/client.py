#!/usr/bin/env python3

import socket, pickle, sys
from card import Card
from network import TCPNetwork

class Client:
	def __innit__(self):
		

def menu():
	print("1 - Rejoindre une partie")
	print("2 - Démarrer une partie")
	print("3 - Quitter")
	return int(input("Choix : "))




########################################################################
############			PROTOTYPES IN UML			####################
########################################################################

# communicate withe the server via udp
# either asks to create a new game or for a list of existing ones to join
def connect_server(host_server, port_server):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.settimeout(10.0)
	msg = "Hello Python!"
	address_game = (host_server, port_server)
	while True:
		c = menu()
		if c == 1:
			msg = "join"
			sock.sendto(msg.encode(),(host_server,port_server))
			try:
				data,addr = sock.recvfrom(1024)
				print ("Received Messages:",pickle.loads(data)," from",addr)
			except socket.timeout:
				print('Request timed out')
			break
		elif c == 2:
			msg = "ng"
			sock.sendto(msg.encode(),(host_server,port_server))
			try:
				data,addr = sock.recvfrom(1024)
				print ("Received Messages:",pickle.loads(data)," from",addr)
			except socket.timeout:
				print('Request timed out')
			break
		elif c == 3:
			break
		else :
			pass
	return address_game

# connect to the chosen game
def connect_game(address_game):
	network = TCPNetwork(address_game)
	network.connect()
	card = Card("","","cardname","","",
	[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],"","","")
	network.send(card)

	print ('Data Sent to Server')

	rcard = network.recv(4096)
		
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

	adress_game = connect_server(host_server, port_server)
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



























