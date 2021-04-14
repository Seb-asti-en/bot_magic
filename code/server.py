#!/usr/bin/env python3

import socket, pickle
from card import Card

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 5000         # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
	socket_server.bind((HOST, PORT))
	socket_server.listen(5)
	conn, address = socket_server.accept()
	
	with conn:
		print('Connected by', address)
		
		while True:
			data = conn.recv(4096)
			if not data:
				break
			data_variable = pickle.loads(data)
			print(data_variable)
			conn.send(data)
				
		conn.close()
		
	socket_server.close()

	print('Data received from client')
        
            
