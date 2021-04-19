#!/usr/bin/env python3

import socket, pickle, sys
from card import Card
from network import TCPNetwork

class Client:
	pass

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


def udp_fct_cli(udp_host="127.0.0.1", udp_port=12345):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	msg = "Hello Python!"
	while True:
		c = (input("Send ? y/n \n"))
		if c == 'y':
			sock.sendto(msg.encode(),(udp_host,udp_port))
			data,addr = sock.recvfrom(1024)
			print ("Received Messages:",data," from",addr)
			sock.sendto(data,addr)
			data,addr = sock.recvfrom(1024)
			print ("Received Messages:",data," from",addr)
		else:
			break




########################################################################
############			PROTOTYPES IN UML			####################
########################################################################

def connect_server(host_server, port_server):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	msg = "Hello Python!"
	address = 1
	while True:
		c = menu()
		if c == 1:
			sock.sendto(msg.encode(),(host_server,port_server))
			data,addr = sock.recvfrom(1024)
			print ("Received Messages:",data," from",addr)
			sock.sendto(data,addr)
			data,addr = sock.recvfrom(1024)
			print ("Received Messages:",data," from",addr)
			break
		elif c == 2:
			break
		elif c == 3:
			break
		else :
			pass
	return address

def connect_game():
	pass

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

	connect_server(host_server, port_server)

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



























