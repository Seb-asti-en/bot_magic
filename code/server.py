#!/usr/bin/env python3

import socket, pickle, sys
from threading import Thread
from card import Card
from game import Game

########################################################################
############			PROTOTYPES IN UML			####################
########################################################################



class Server:
	def __init__(self, server_address, server_port):
		self.__server_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__server_info	= (server_address, server_port)
		self.__list_games	= []

	def threaded_func(self, game):
		print ("hello thread started: ")
		print (game.get_socket())
		game.wait_client();
		game.start()


	def run(self):
		self.__server_socket.bind(self.__server_info)
		i=0
		while True:
			i+=1
			print ("Waiting for client...")
			data,addr = self.__server_socket.recvfrom(1024)
			print ("Received Messages:",data," from",addr)
			if data.decode() == "load":
				host_game, port_game = "localhost", 4444+i
				self.create_game(host_game, port_game)
				self.__server_socket.sendto(pickle.dumps((host_game, port_game)),addr)
			if data.decode() == "ng":
				host_game, port_game = "localhost", 4444+i
				self.create_game(host_game, port_game)
				self.__server_socket.sendto(pickle.dumps((host_game, port_game)),addr)
			else:
				self.__server_socket.sendto(pickle.dumps("come back when you wanna do someting"),addr)
	#		data,addr = self.__server_socket.recvfrom(1024)
	#		print ("Received Messages:",data," from",addr)
	#		self.__server_socket.sendto(data,addr)

	def create_game(self, host_server, port_server):
		print ("create_game")
		game = Game(host_server, port_server)
		Thread(target=self.threaded_func, args = (game,)).start()
		print ("thead created")

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

	
#	socket.gethostname()
	host_server = str(sys.argv[1])
	port_server = int(sys.argv[2])

	if port_server < 1024:
		print("Port invalide")
		sys.exit(-1)
	
	server = Server(host_server, port_server)
	server.run()

#	Thread(target=udp_fct_serv, args=(host_server, port_server)).start()



		

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print ('Interrupted')
		sys.exit(0)

























