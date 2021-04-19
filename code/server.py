#!/usr/bin/env python3

import socket, pickle, sys
from threading import Thread
from card import Card


########################################################################
############			PROTOTYPES IN UML			####################
########################################################################

def run(host_server, port_server):
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind((host_server,port_server))
	while True:
		print ("Waiting for client...")
		data,addr = sock.recvfrom(1024)
		print ("Received Messages:",data," from",addr)
		if data.decode() == "ng":
			#Thread(target=create_game, args=(host_server, port_server)).start()
			sock.sendto(pickle.dumps((host_server, port_server)),addr)
		else:
			sock.sendto(pickle.dumps("come back when you wanna do someting"),addr)
#		data,addr = sock.recvfrom(1024)
#		print ("Received Messages:",data," from",addr)
#		sock.sendto(data,addr)

def create_game(host_server, port_server):
	socket_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_game.bind((host_server, port_server))
	socket_game.listen(5)
	while True:
		conn, address = socket_game.accept()
		print('Connected by', address)
#			Thread(target=threaded_func, args=(conn,address)).start()
	socket_game.close()

def send_action():
	pass

def receive_action():
	pass

########################################################################

#def udp_fct_serv(host_server, port_server):
#	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#	msg = "Hello Python!"
#	sock.bind((host_server,port_server))
#	while True:
#		print ("Waiting for client...")
#		data,addr = sock.recvfrom(1024)
#		print ("Received Messages:",data," from",addr)
#		sock.sendto(data,addr)
#		create_game(host_server, port_server)
##		data,addr = sock.recvfrom(1024)
#		print ("Received Messages:",data," from",addr)
#		sock.sendto(data,addr)


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
#	socket_server.bind((host_server, port_server))
#	socket_server.listen(5)
#	conn, address = socket_server.accept()
#	conn.close()
#	socket_server.close()

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

	run(host_server, port_server)

#	Thread(target=udp_fct_serv, args=(host_server, port_server)).start()



		

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)

























