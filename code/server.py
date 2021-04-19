#!/usr/bin/env python3

import socket, pickle, sys
from threading import Thread
from card import Card


########################################################################
############			PROTOTYPES IN UML			####################
########################################################################

def run():
	pass

def create_game():
	pass

def send_action():
	pass

def receive_action():
	pass

########################################################################

def udp_fct_serv(udp_host="127.0.0.1", udp_port=12345):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	msg = "Hello Python!"
	sock.bind((udp_host,udp_port))
	while True:
		print ("Waiting for client...")
		data,addr = sock.recvfrom(1024)
		print ("Received Messages:",data," from",addr)
		sock.sendto(data,addr)
		data,addr = sock.recvfrom(1024)
		print ("Received Messages:",data," from",addr)
		sock.sendto(data,addr)


#
def threaded_func(conn, address):
	while True:
		data = conn.recv(4096)
		if not data:
			break
		data_variable = pickle.loads(data)
		print('Data received from client :')
		print(data_variable)
		conn.send(data)
	conn.close()
	
#	socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
#	socket_server.bind((hostServer, portServer))
#	socket_server.listen(5)
#	conn, address = socket_server.accept()
#	conn.close()
#	socket_server.close()

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

	Thread(target=udp_fct_serv).start()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
		socket_server.bind((hostServer, portServer))
		socket_server.listen(5)
		
		while True:
			conn, address = socket_server.accept()
			print('Connected by', address)
			Thread(target=threaded_func, args=(conn,address)).start()
		
		socket_server.close()

		

if __name__ == "__main__":
	main()


























