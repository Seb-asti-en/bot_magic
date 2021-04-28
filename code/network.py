import socket
import pickle

class TCPNetwork:
	# create static method
	@staticmethod
	def connect(self, info):
		try:
			self.client.connect(info)
		except:
			pass
	@staticmethod
	def send(sock, data):
		try:
			sock.send(pickle.dumps(data))
		except socket.error as e:
			print(e)

	@staticmethod
	def recv(sock, size = 4096):
		return pickle.loads(sock.recv(size))



class UDPNetwork:
	
	@staticmethod
	def connect(sock, addr):
		try:
			sock.connect(addr)
		except:
			pass

	@staticmethod
	def sendto(sock, data):
		try:
			sock.sendto(pickle.dumps(data))
		except socket.error as e:
			print(e)

	@staticmethod
	def recvfrom(sock, size = 4096):
		return pickle.loads(sock.recv(size))
